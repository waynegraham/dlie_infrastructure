from celery import Celery
from celery.schedules import crontab
import requests
from tika import parser
from datetime import datetime
import os
import boto3
import psycopg2
import feedparser

# Base directories (with defaults)
OAI_DIR = os.getenv('OAI_DIR', './data/oai')
RSS_DIR = os.getenv('RSS_DIR', './data/rss')

# Ensure directories exist
os.makedirs(OAI_DIR, exist_ok=True)
os.makedirs(RSS_DIR, exist_ok=True)

# Initialize Celery with RabbitMQ broker
app = Celery('etl_tasks', broker='amqp://guest@rabbitmq//')

# Environment/configuration
S3_BUCKET = os.getenv('S3_BUCKET', 'integral-ecology-bucket')
DB_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@db:5432/library')

# Initialize AWS S3 client
s3 = boto3.client('s3')

# Database connection helper
def get_db_conn():
    return psycopg2.connect(DB_URL)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Run daily OAI harvesting at 02:00 UTC
    sender.add_periodic_task(
        crontab(hour=2, minute=0),
        harvest_oai.s('https://doaj.org/oai', 'doaj')
    )
    # Run daily RSS harvesting at 03:00 UTC
    sender.add_periodic_task(
        crontab(hour=3, minute=0),
        harvest_rss.s('https://www.ecologyandsociety.org/feed/')
    )

@app.task
def harvest_oai(base_url, prefix):
    """Harvest records via OAI-PMH and store raw XML in S3."""
    params = {'verb': 'ListRecords', 'metadataPrefix': 'oai_dc'}
    response = requests.get(base_url, params=params)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    filename = f"{prefix}_oai_{timestamp}.xml"
    filepath = os.path.join(OAI_DIR, filename)
    with open(filepath, 'wb') as f:
        f.write(response.content)
    print(f"Saved OAI feed to {filepath}")
    # key = f"{prefix}/oai_{datetime.utcnow().isoformat()}.xml"
    # s3.put_object(Bucket=S3_BUCKET, Key=key, Body=response.content)
    print(f"Saved OAI feed to {filepath}")


@app.task
def harvest_rss(rss_url):
    """Fetch RSS feed entries, download PDFs, extract text via Tika, and store in S3."""
    feed = feedparser.parse(rss_url)
    for entry in feed.entries:
        pdf_url = entry.get('link')
        if pdf_url and pdf_url.endswith('.pdf'):
            response = requests.get(pdf_url)
            filename = pdf_url.split('/')[-1]
            with open(filename, 'wb') as f:
                f.write(response.content)
            parsed = parser.from_file(filename)
            text = parsed.get('content', [''])[0]
            key = f"pdf/{filename}.txt"
            # s3.put_object(Bucket=S3_BUCKET, Key=key, Body=text.encode('utf-8'))
            # os.remove(filename)
            txt_filename = pdf_filename + '.txt'
            txt_path = os.path.join(RSS_DIR, txt_filename)
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Processed and stored {txt_filename}")