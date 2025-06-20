import json
import logging
import os
from datetime import datetime

from celery import Celery
from celery.schedules import crontab
import feedparser
import pandas as pd  # for CSV processing
import requests
from tika import parser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.models import ResourceModel as Resource

logger = logging.getLogger(__name__)
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
app = Celery('etl_tasks', broker=os.getenv('BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//'))

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Ensure data directories exist before scheduling
    for d in (OAI_DIR, RSS_DIR, API_DIR):
        os.makedirs(d, exist_ok=True)
    # Every day at 02:00 UTC
    sender.add_periodic_task(crontab(hour=2, minute=0), harvest_oai.s('https://doaj.org/oai', 'doaj'))
    # Every day at 03:00 UTC
    sender.add_periodic_task(crontab(hour=3, minute=0), harvest_rss.s('https://www.ecologyandsociety.org/rss'))
    # Every day at 04:00 UTC
    sender.add_periodic_task(crontab(hour=4, minute=0), harvest_api.s('http://api:8000/resources'))


@app.task
def harvest_oai(base_url, prefix):
    """OAI-PMH harvest → raw XML"""
    os.makedirs(OAI_DIR, exist_ok=True)
    resp = requests.get(base_url, params={'verb':'ListRecords','metadataPrefix':'oai_dc'})
    fn = f"{prefix}_oai_{datetime.utcnow():%Y%m%d%H%M%S}.xml"
    path = os.path.join(OAI_DIR, fn)
    with open(path,'wb') as f:
        f.write(resp.content)
    logger.info("OAI harvest saved XML to %s", path)

@app.task
def harvest_rss(rss_url):
    """RSS harvest → download PDFs → extract text"""
    os.makedirs(RSS_DIR, exist_ok=True)
    feed = feedparser.parse(rss_url)
    for e in feed.entries:
        link = e.get('link') or ''
        if link.lower().endswith('.pdf'):
            pdf = requests.get(link).content
            name = os.path.basename(link)
            pdf_path = os.path.join(RSS_DIR, name)
            with open(pdf_path,'wb') as f:
                f.write(pdf)
            text = parser.from_file(pdf_path).get('content', [''])[0]
            txt_path = os.path.join(RSS_DIR, name + '.txt')
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)
            logger.info("RSS harvest processed PDF %s", name)

@app.task
def harvest_api(api_url):
    """API harvest → JSON dump"""
    os.makedirs(API_DIR, exist_ok=True)
    resp = requests.get(api_url)
    data = resp.json()
    fn = f"api_{datetime.utcnow():%Y%m%d%H%M%S}.json"
    path = os.path.join(API_DIR, fn)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    logger.info("API harvest saved JSON to %s", path)

@app.task(name='load_integral_ecology')
def load_integral_ecology():
    """Load OpenAlex integral ecology resources into the database."""
    csv_path = OPEN_ALEX_CSV
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    count = 0
    for _, row in df.iterrows():
        res = Resource(
            title=row.get('title'),
            type=row.get('type'),
            date=row.get('date'),
            authors=[a.strip() for a in row.get('authors', '').split(';') if a.strip()],
            abstract=row.get('abstract'),
            doi=row.get('doi'),
            url=row.get('url'),
            keywords=[k.strip() for k in row.get('keywords', '').split(';') if k.strip()],
            provider=row.get('provider'),
            fulltext=row.get('fulltext')
        )
        db.add(res)
        count += 1
        if count % 500 == 0:
            db.commit()
    db.commit()
    db.close()
    logger.info("OpenAlex loader loaded %d resources from %s", count, csv_path)
