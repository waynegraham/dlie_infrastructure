import os
import json
from datetime import datetime
import requests
import feedparser
from tika import parser
from celery import Celery
from celery.schedules import crontab

# Configure output directories
OAI_DIR = os.getenv('OAI_DIR', './data/oai')
RSS_DIR = os.getenv('RSS_DIR', './data/rss')
API_DIR = os.getenv('API_DIR', './data/api')
for d in (OAI_DIR, RSS_DIR, API_DIR):
    os.makedirs(d, exist_ok=True)

# Celery app (make sure BROKER_URL is set to amqp://guest:guest@rabbitmq:5672//)
app = Celery('etl_tasks', broker=os.getenv('BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//'))

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Every day at 02:00 UTC
    sender.add_periodic_task(crontab(hour=2, minute=0), harvest_oai.s('https://doaj.org/oai', 'doaj'))
    # Every day at 03:00 UTC
    sender.add_periodic_task(crontab(hour=3, minute=0), harvest_rss.s('https://www.ecologyandsociety.org/rss'))
    # Every day at 04:00 UTC
    sender.add_periodic_task(crontab(hour=4, minute=0), harvest_api.s('http://api:8000/resources'))

@app.task
def harvest_oai(base_url, prefix):
    """OAI-PMH harvest → raw XML"""
    resp = requests.get(base_url, params={'verb':'ListRecords','metadataPrefix':'oai_dc'})
    fn = f"{prefix}_oai_{datetime.utcnow():%Y%m%d%H%M%S}.xml"
    path = os.path.join(OAI_DIR, fn)
    with open(path,'wb') as f: f.write(resp.content)
    print(f"[OAI] saved {path}")

@app.task
def harvest_rss(rss_url):
    """RSS harvest → download PDFs → extract text"""
    feed = feedparser.parse(rss_url)
    for e in feed.entries:
        link = e.get('link') or ''
        if link.lower().endswith('.pdf'):
            pdf = requests.get(link).content
            name = os.path.basename(link)
            pdf_path = os.path.join(RSS_DIR, name)
            with open(pdf_path,'wb') as f: f.write(pdf)
            text = parser.from_file(pdf_path).get('content',[''])[0]
            txt_path = os.path.join(RSS_DIR, name+'.txt')
            with open(txt_path,'w',encoding='utf-8') as f: f.write(text)
            print(f"[RSS] processed {name}")

@app.task
def harvest_api(api_url):
    """API harvest → JSON dump"""
    resp = requests.get(api_url)
    data = resp.json()
    fn = f"api_{datetime.utcnow():%Y%m%d%H%M%S}.json"
    path = os.path.join(API_DIR, fn)
    with open(path,'w',encoding='utf-8') as f: json.dump(data, f, indent=2)
    print(f"[API] saved {path}")