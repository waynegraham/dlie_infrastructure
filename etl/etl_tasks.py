import json
import logging
import os
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Union

try:
    from celery import Celery
    from celery.schedules import crontab
except ImportError:
    # allow import without celery installed (e.g. for tests)
    class _DummySignal:
        @staticmethod
        def connect(f):
            return f

    class Celery:
        on_after_configure = _DummySignal()

        def __init__(self, *args, **kwargs):
            pass

        def task(self, *args, **kwargs):
            # support both @app.task and @app.task(...)
            if args and callable(args[0]):
                return args[0]
            def decorator(fn):
                return fn

            return decorator

        def config_from_object(self, *args, **kwargs):
            # no-op for tests without celery installed
            return None

    def crontab(*args, **kwargs):
        return None
import feedparser
import pandas as pd  # for CSV processing
import requests
from tika import parser
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.models import ResourceModel as Resource

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
HTTP_TIMEOUT = int(os.getenv('HTTP_TIMEOUT', '10'))  # seconds for HTTP requests

# configure HTTP retries/backoff for all GET requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

HTTP_RETRIES = int(os.getenv('HTTP_RETRIES', '3'))
HTTP_BACKOFF_FACTOR = float(os.getenv('HTTP_BACKOFF_FACTOR', '0.3'))
_retry_strategy = Retry(
    total=HTTP_RETRIES,
    backoff_factor=HTTP_BACKOFF_FACTOR,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
_http_adapter = HTTPAdapter(max_retries=_retry_strategy)
_session = requests.Session()
_session.mount("http://", _http_adapter)
_session.mount("https://", _http_adapter)
# route requests.get through session to apply retries/backoff
requests.get = _session.get

# harvest schedule and endpoint configuration via environment variables
OAI_DIR = Path(os.getenv('OAI_DIR', './data/oai'))
RSS_DIR = Path(os.getenv('RSS_DIR', './data/rss'))
API_DIR = Path(os.getenv('API_DIR', './data/api'))
OPEN_ALEX_CSV = Path(os.getenv(
    'OPEN_ALEX_CSV', './data/openalex/updated_integral_ecology_with_fulltext.csv'
))

# OAI-PMH harvest config
OAI_BASE_URL = os.getenv('OAI_BASE_URL', 'https://doaj.org/oai')
OAI_PREFIX = os.getenv('OAI_PREFIX', 'doaj')
OAI_SCHEDULE_HOUR = int(os.getenv('OAI_SCHEDULE_HOUR', '2'))
OAI_SCHEDULE_MINUTE = int(os.getenv('OAI_SCHEDULE_MINUTE', '0'))

# RSS harvest config
RSS_URL = os.getenv('RSS_URL', 'https://www.ecologyandsociety.org/rss')
RSS_SCHEDULE_HOUR = int(os.getenv('RSS_SCHEDULE_HOUR', '3'))
RSS_SCHEDULE_MINUTE = int(os.getenv('RSS_SCHEDULE_MINUTE', '0'))

# API harvest config
API_URL = os.getenv('API_URL', 'http://api:8000/resources')
API_SCHEDULE_HOUR = int(os.getenv('API_SCHEDULE_HOUR', '4'))
API_SCHEDULE_MINUTE = int(os.getenv('API_SCHEDULE_MINUTE', '0'))

def _atomic_write_bytes(path: Union[Path, str], data: bytes) -> None:
    path = Path(path)
    dirpath = path.parent
    with tempfile.NamedTemporaryFile(delete=False, dir=str(dirpath)) as tf:
        tf.write(data)
        tf.flush()
        os.fsync(tf.fileno())
    os.replace(tf.name, str(path))

def _atomic_write_text(path: Union[Path, str], text: str, encoding: str = 'utf-8') -> None:
    path = Path(path)
    dirpath = path.parent
    with tempfile.NamedTemporaryFile(delete=False, dir=str(dirpath), mode='w', encoding=encoding) as tf:
        tf.write(text)
        tf.flush()
        os.fsync(tf.fileno())
    os.replace(tf.name, str(path))
OAI_DIR = os.getenv('OAI_DIR', './data/oai')
RSS_DIR = os.getenv('RSS_DIR', './data/rss')
API_DIR = os.getenv('API_DIR', './data/api')
OPEN_ALEX_CSV = os.getenv('OPEN_ALEX_CSV', './data/openalex/updated_integral_ecology_with_fulltext.csv')

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://my_user:my_pass@db:5432/my_database"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


# Celery app (make sure BROKER_URL is set to amqp://guest:guest@rabbitmq:5672//)
app = Celery('etl_tasks')
# load broker_url & beat_schedule from celeryconfig.py
app.config_from_object('etl.celeryconfig')


@app.task
def harvest_oai(base_url, prefix):
    """OAI-PMH harvest → raw XML, with resumptionToken support."""
    OAI_DIR.mkdir(parents=True, exist_ok=True)
    params = {'verb': 'ListRecords', 'metadataPrefix': 'oai_dc'}
    page = 0
    while True:
        try:
            resp = requests.get(base_url, params=params, timeout=HTTP_TIMEOUT)
            resp.raise_for_status()
            ts = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
            fn = f"{prefix}_oai_{ts}_{page}.xml"
            path = OAI_DIR / fn
            _atomic_write_bytes(path, resp.content)
            logger.info("OAI harvest saved XML to %s", path)
            # parse for resumptionToken to fetch next batch
            try:
                root = ET.fromstring(resp.content)
                token = None
                for elem in root.iter():
                    if elem.tag.endswith('resumptionToken'):
                        token = (elem.text or '').strip()
                        break
            except Exception:
                logger.exception("Failed to parse OAI response for resumptionToken %s", path)
                break
            if not token:
                break
            params = {'verb': 'ListRecords', 'resumptionToken': token}
            page += 1
        except Exception:
            logger.exception("OAI harvest failed for %s", base_url)
            break

@app.task
def harvest_rss(rss_url):
    """RSS harvest → download PDFs → extract text"""
    RSS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        feed = feedparser.parse(rss_url)
    except Exception:
        logger.exception("Failed to parse RSS feed %s", rss_url)
        return
    for e in feed.entries:
        link = e.get('link') or ''
        if link.lower().endswith('.pdf'):
            try:
                resp = requests.get(link, timeout=HTTP_TIMEOUT)
                resp.raise_for_status()
                pdf = resp.content
                name = os.path.basename(link)
                pdf_path = RSS_DIR / name
                _atomic_write_bytes(pdf_path, pdf)
                text = parser.from_file(pdf_path).get('content', [''])[0]
                txt_path = RSS_DIR / f"{name}.txt"
                _atomic_write_text(txt_path, text, encoding='utf-8')
                logger.info("RSS harvest processed PDF %s", name)
            except Exception:
                logger.exception("RSS harvest failed for PDF %s", link)

@app.task
def harvest_api(api_url):
    """API harvest → JSON dump"""
    API_DIR.mkdir(parents=True, exist_ok=True)
    try:
        resp = requests.get(api_url, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        fn = f"api_{datetime.now(timezone.utc):%Y%m%d%H%M%S}.json"
        path = API_DIR / fn
        text = json.dumps(data, indent=2)
        _atomic_write_text(path, text, encoding='utf-8')
        logger.info("API harvest saved JSON to %s", path)
    except Exception:
        logger.exception("API harvest failed for %s", api_url)


@app.task(name='prune_old_harvests')
def prune_old_harvests():
    """Prune raw harvest files older than RETENTION_DAYS in OAI, RSS, and API dirs."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
    for directory in (OAI_DIR, RSS_DIR, API_DIR):
        for file in directory.iterdir():
            try:
                if file.is_file() and datetime.fromtimestamp(file.stat().st_mtime, timezone.utc) < cutoff:
                    file.unlink()
                    logger.info("Pruned old file %s", file)
            except Exception:
                logger.exception("Failed to prune file %s", file)

@app.task(name='load_integral_ecology')
def load_integral_ecology():
    """Load OpenAlex integral ecology resources into the database."""
    csv_path = OPEN_ALEX_CSV
    count = 0
    chunk_size = int(os.getenv('ETL_CHUNK_SIZE', '500'))
    with SessionLocal() as db:
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            mappings = []
            for _, row in chunk.iterrows():
                # parse date strings into Python date objects for SQLite Date columns
                raw_date = row.get('date')
                if isinstance(raw_date, str):
                    try:
                        parsed_date = datetime.fromisoformat(raw_date).date()
                    except ValueError:
                        parsed_date = None
                else:
                    parsed_date = raw_date
                mappings.append({
                    'title': row.get('title'),
                    'resource_type': row.get('type'),
                    'date': parsed_date,
                    'authors': [
                        a.strip() for a in row.get('authors', '').split(';') if a.strip()
                    ],
                    'abstract': row.get('abstract'),
                    'doi': row.get('doi'),
                    'url': row.get('url'),
                    'keywords': [
                        k.strip() for k in row.get('keywords', '').split(';') if k.strip()
                    ],
                    'provider': row.get('provider'),
                    'fulltext': row.get('fulltext'),
                })
            db.bulk_insert_mappings(Resource, mappings)
            db.commit()
            count += len(mappings)
    logger.info(
        "OpenAlex loader loaded %d resources from %s", count, csv_path
    )
