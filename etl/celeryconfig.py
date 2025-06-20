# Celery configuration for periodic ETL tasks.
import os
try:
    from celery.schedules import crontab
except ImportError:
    # allow import without celery installed (e.g. for tests)
    def crontab(*args, **kwargs):
        return None

# Broker URL (e.g. amqp://guest:guest@rabbitmq:5672//)
broker_url = os.getenv('BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//')

# OAI-PMH harvest configuration
OAI_BASE_URL = os.getenv('OAI_BASE_URL', 'https://doaj.org/oai')
OAI_PREFIX = os.getenv('OAI_PREFIX', 'doaj')
OAI_SCHEDULE_HOUR = int(os.getenv('OAI_SCHEDULE_HOUR', '2'))
OAI_SCHEDULE_MINUTE = int(os.getenv('OAI_SCHEDULE_MINUTE', '0'))

# RSS harvest configuration
RSS_URL = os.getenv('RSS_URL', 'https://www.ecologyandsociety.org/rss')
RSS_SCHEDULE_HOUR = int(os.getenv('RSS_SCHEDULE_HOUR', '3'))
RSS_SCHEDULE_MINUTE = int(os.getenv('RSS_SCHEDULE_MINUTE', '0'))

# API harvest configuration
API_URL = os.getenv('API_URL', 'http://api:8000/resources')
API_SCHEDULE_HOUR = int(os.getenv('API_SCHEDULE_HOUR', '4'))
API_SCHEDULE_MINUTE = int(os.getenv('API_SCHEDULE_MINUTE', '0'))

# Celery Beat schedule
beat_schedule = {
    'harvest-oai': {
        'task': 'etl.etl_tasks.harvest_oai',
        'schedule': crontab(hour=OAI_SCHEDULE_HOUR, minute=OAI_SCHEDULE_MINUTE),
        'args': (OAI_BASE_URL, OAI_PREFIX),
    },
    'harvest-rss': {
        'task': 'etl.etl_tasks.harvest_rss',
        'schedule': crontab(hour=RSS_SCHEDULE_HOUR, minute=RSS_SCHEDULE_MINUTE),
        'args': (RSS_URL,),
    },
    'harvest-api': {
        'task': 'etl.etl_tasks.harvest_api',
        'schedule': crontab(hour=API_SCHEDULE_HOUR, minute=API_SCHEDULE_MINUTE),
        'args': (API_URL,),
    },
    # prune old raw harvest files daily
    'prune-old-harvests': {
        'task': 'etl.etl_tasks.prune_old_harvests',
        'schedule': crontab(hour=0, minute=30),
        'args': (),
    },
}
