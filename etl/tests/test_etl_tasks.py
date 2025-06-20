# -*- coding: utf-8 -*-
"""Unit tests for the ETL Celery tasks."""
import os
import csv
import json
import importlib

import pytest

# Dummy HTTP response for requests.get
class DummyResponse:
    def __init__(self, content=None, json_data=None):
        self.content = content
        self._json = json_data

    def json(self):
        return self._json


@pytest.fixture(autouse=True)
def reload_tasks(tmp_path, monkeypatch):
    """
    Reloads the etl_tasks module with fresh environment variables so
    directory constants and database URL pick up tmp_path values.
    """
    # Configure directories and CSV path in a temporary location
    monk_env = monkeypatch.setenv
    monk_env('OAI_DIR', str(tmp_path / 'oai'))
    monk_env('RSS_DIR', str(tmp_path / 'rss'))
    monk_env('API_DIR', str(tmp_path / 'api'))
    monk_env('OPEN_ALEX_CSV', str(tmp_path / 'data.csv'))
    # Use an on-disk SQLite DB for tests
    db_file = tmp_path / 'test.db'
    monk_env('DATABASE_URL', f'sqlite:///{db_file}')

    # Reload module so OAI_DIR, RSS_DIR, API_DIR, OPEN_ALEX_CSV, DATABASE_URL reset
    import etl.etl_tasks as tasks_mod
    tasks = importlib.reload(tasks_mod)
    return tasks


def test_harvest_oai(tmp_path, reload_tasks, monkeypatch):
    tasks = reload_tasks
    xml_data = b'<root>ok</root>'
    monkeypatch.setattr(tasks.requests, 'get', lambda url, params=None: DummyResponse(content=xml_data))
    tasks.harvest_oai('http://fake', 'prefix')
    files = list((tmp_path / 'oai').iterdir())
    assert len(files) == 1
    assert files[0].read_bytes() == xml_data


def test_harvest_rss(tmp_path, reload_tasks, monkeypatch):
    tasks = reload_tasks
    # Fake feed with one PDF link
    monkeypatch.setattr(tasks.feedparser, 'parse', lambda url: type('F', (), {'entries': [{'link': 'http://x/test.pdf'}]})())
    pdf_bytes = b'%PDF-1.4 content'
    monkeypatch.setattr(tasks.requests, 'get', lambda url: DummyResponse(content=pdf_bytes))
    monkeypatch.setattr(tasks.parser, 'from_file', lambda path: {'content': ['text content']})
    tasks.harvest_rss('ignored')
    pdfs = list((tmp_path / 'rss').glob('*.pdf'))
    txts = list((tmp_path / 'rss').glob('*.txt'))
    assert len(pdfs) == 1
    assert pdfs[0].read_bytes() == pdf_bytes
    assert len(txts) == 1
    assert txts[0].read_text(encoding='utf-8') == 'text content'


def test_harvest_api(tmp_path, reload_tasks, monkeypatch):
    tasks = reload_tasks
    payload = {'k': 'v'}
    monkeypatch.setattr(tasks.requests, 'get', lambda url: DummyResponse(json_data=payload))
    tasks.harvest_api('ignored')
    files = list((tmp_path / 'api').glob('*.json'))
    assert len(files) == 1
    assert json.loads(files[0].read_text(encoding='utf-8')) == payload


def test_load_integral_ecology(tmp_path, reload_tasks):
    tasks = reload_tasks
    # Prepare a minimal CSV
    csv_path = tmp_path / 'data.csv'
    row = {
        'title': 'T', 'type': 'paper', 'date': '2020-01-01',
        'authors': 'A;B', 'abstract': 'abs', 'doi': '', 'url': '',
        'keywords': 'k1;k2', 'provider': 'p', 'fulltext': 'ft'
    }
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)

    # Create DB schema using the API Base
    from api.database import Base
    Base.metadata.create_all(reload_tasks.engine)

    # Run loader and verify one record inserted
    reload_tasks.load_integral_ecology()
    session = reload_tasks.SessionLocal()
    results = session.query(reload_tasks.Resource).all()
    assert len(results) == 1
    r = results[0]
    assert r.title == 'T'
    assert isinstance(r.authors, list) and r.authors == ['A', 'B']
    session.close()