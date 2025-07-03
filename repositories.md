# GIS

## Natural Earth 

Public domain (CC0) cultural, physical, and raster layers at 1:10 m, 1:50 m, and 1:110 m scales.

### Access Methods

* Bulk download from [Github](https://github.com/nvkelso/natural-earth-vector)
* Individual shapefiles

### Bulk download and unzip

```python
import requests, zipfile, io

url = 'https://github.com/nvkelso/natural-earth-vector/archive/refs/heads/master.zip'
resp = requests.get(url)
resp.raise_for_status()

# Extract only the 1_50m cultural layers
with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
    for member in z.namelist():
        if 'ne_50m_admin_0_countries.shp' in member:
            z.extract(member, path='data/natural_earth')

# Unzip using geopandas or zipfile module
```

* Check upstream GitHub releases quarterly for new version; can automate via Github API or RSS feed.

## Open Street Map

Is this needed? Can get from AWS (`s3://osm-pds/planet/planet-latest.osm.pbf`) or Geofabrik (<download.geofabrik.de>)

If needed, monthly full dump.

## GADM (Global Administrative Areas)

Multi-level boundaries for >250 countries. 

### Access Methods

* Bulk download (zip per country) <https://gadm.org/download_country.html>

```python
import requests

country_iso = 'USA'  # Change to desired ISO code
url = f'https://geodata.ucdavis.edu/gadm/gadm4.1/shp/gadm41_shp.zip'
resp = requests.get(url)
resp.raise_for_status()
with open('data/gadm41_shp.zip', 'wb') as f:
    f.write(resp.content)
# Unzip using geopandas or zipfile module
```

Major releases are roughly annually. Check once a year and compare checksums.

# Time-Series & Monitoring Networks

## Global Biodiversity Information Facility (GBIF)

Provides species occurrence with geospatial and timestamp metadata. CC0

### Access Methods

* REST API: JSON or DwC-A download via HTTP.
* Bulk download: Darwin Core Archive (DwC-A) via GBIF data download service.

```python
import requests

def fetch_gbif_occurrences(taxon_key, year_from, year_to, limit=300):
    url = 'https://api.gbif.org/v1/occurrence/search'
    params = {
        'taxonKey': taxon_key,
        'year': f'{year_from},{year_to}',
        'limit': limit,
        'hasCoordinate': True
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()['results']

# Example: fetch up to 300 records for taxon 212 (Fagus) from 2020–2025
data = fetch_gbif_occurrences(212, 2020, 2025)
print(f"Fetched {len(data)} occurrence records")
```

### Bulk Download (DwC‑A)

* Use the GBIF download API endpoint:
  * POST a download request JSON to `https://api.gbif.org/v1/occurrence/download/request`.
  * Poll status and fetch zip when ready.

### Update

* GBIF updates daily; schedule downloads or API syncs monthly for full datasets, weekly for targeted taxon queries.

## FLUXNET

Ecosystem CO₂, water, and energy flux tower measurements globally.

### Access Methods

* Site Data Portal: HTTP bulk downloads by site or network.
* API access: via FLUXNET 2015/2019 data web services (level‑ready).

> Example for a single site CSV

```python
import requests
from pathlib import Path

site_id = 'US-UMB'  # e.g., University of Michigan Biological Station
url = f'https://fluxnet.fluxdata.org/data/fluxnet2015/{site_id}.csv'
resp = requests.get(url)
resp.raise_for_status()
path = Path('data/fluxnet') / f'{site_id}.csv'
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(resp.content)
print(f"Downloaded {site_id} data ({path.stat().st_size} bytes)")
```

### Bulk Download

FLUXNET publishes annual zipped datasets; request via email or portal, then download via HTTP.

### Update Cadence

Data augmented annually; schedule annual refreshes after new release announcements (typically Q1).

## World Bank Open Data

Socio‑economic and environmental time‑series indicators (GDP, population, CO₂ emissions, etc.).

### Access Methods

* REST API: JSON or XML.
* Bulk CSV: per‑indicator or full dumps via data catalog.

Example: Fetching Indicator Time‑Series

```python
import requests
import pandas as pd

def fetch_indicator(indicator, country_code='all', start_year=2000, end_year=2023):
    url = f'https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}'
    params = {'date': f'{start_year}:{end_year}', 'format': 'json', 'per_page': 10000}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()[1]
    return pd.DataFrame(data)

# Example: CO2 emissions (metric tons per capita) 2000–2023 for all countries
df = fetch_indicator('EN.ATM.CO2E.PC', start_year=2000, end_year=2023)
print(df.head())
```

### Bulk Download

Full indicator CSVs: https://databank.worldbank.org/data/download/FILEMANAGER/API_CSV.zip

### Update Cadence

Indicators updated quarterly; schedule quarterly syncs.

# Remote-Sensing Imagery & Raster

## NASA Earthdata (MODIS & VIIRS)

Products (e.g. MOD09GA, VIIRS L2) are public domain under NASA policy.

### Access Methods

* STAC API (CMR): Query Earthdata Collections via STAC endpoints.
* HTTPS Bulk: AWS Open Data Registry (s3://modis-orr/, s3://noaa-viirs/).
* Earthdata Login: Required for some endpoints; use credentials with netrc or requests auth

### Example: STAC Search & Download

```python
import requests, os
# STAC endpoint for MODIS
url = 'https://cmr.earthdata.nasa.gov/stac/search'
params = {
    'collections': 'MODIS_006_MOD09GA',
    'bbox': [-180, -90, 180, 90],
    'datetime': '2024-01-01/2024-01-31',
    'limit': 10
}
resp = requests.post(url, json=params)
resp.raise_for_status()
items = resp.json()['features']
for item in items:
    href = item['assets']['reflectance']['href']
    os.system(f"curl -n -O {href}")
```

### Update Cadence

Daily for new scenes; schedule daily STAC sync or AWS crawl.

## ESA Copernicus Open Access Hub (Sentinel‑1/2/3)

Free, CC‑BY‑compatible; global SAR and optical imagery with 5–12 day revisit.

### Access Methods

* OpenSearch API: EarthSearch endpoints for querying by AOI, date, and product type.
* Bulk SAFE Download: Python clients like sentinelsat or direct wget/aria2c.
* STAC (CI Hub): Community STAC catalogs via https://earth-search.aws.element84.com.

### Example: Download Sentinel‑2 Tile

```python
from sentinelsat import SentinelAPI
api = SentinelAPI('user','pass','https://scihub.copernicus.eu/dhus')
products = api.query(
    area='POLYGON((-10 35, -10 45, 0 45, 0 35, -10 35))',
    date=('20240501', '20240531'),
    platformname='Sentinel-2', producttype='S2MSI1C'
)
for prod_id, metadata in products.items():
    api.download(prod_id, directory_path='data/sentinel2')
```

### Update Cadence

Sentinel‑2: 5 days; Sentinel‑1: 6 days. Schedule weekly harvests.

## USGS Earth Explorer (Landsat/ASTER/SRTM)

Landsat (since 1972), ASTER, SRTM DEMs—all public domain (USGS/NASA).

### Access Methods

* USGS API: Requires registration; use landsatxplore or direct REST.
* AWS Public Data: s3://landsat-pds/, s3://aster-pds/, s3://usgs-srtm/.
* Bulk via HTTP: EarthExplorer interface or AWS CLI.

### Example: AWS Python Download

```python
import boto3, botocore
s3 = boto3.client('s3')
bucket, key = 'landsat-pds', 'c1/L8/123/045/LC08_L1TP_123045_20240415_20240501_02_T1/LC08_L1TP_123045_20240415_20240501_02_T1_B4.TIF'
s3.download_file(bucket, key, 'data/landsat/B4.TIF')
```

### Update Cadence

Landsat: 16 days per path/row; SRTM: static; ASTER: as‑released. Schedule monthly checks for new scenes.

# Model Archives & Workflows

## Hugging Face Model Hub (Ecology Tag)

Includes species distribution models, ecosystem forecasting pipelines, and Jupyter/R scripts.

### Access Methods

* Hugging Face API (REST): Retrieve model metadata by tag and download via git lfs or hf_hub_download client.
* Hub RSS & Webhooks: Monitor new models in the “ecology” tag

### Example: List Ecology Models & Download

```python
from huggingface_hub import HfApi, hf_hub_download

api = HfApi()
# Search for models tagged 'ecology'
models = api.list_models(filter="tags:ecology", sort="lastModified", direction=-1, limit=20)
for m in models:
    print(f"Model: {m.modelId}, Last modified: {m.lastModified}")
    # Download a specific file (e.g., model card) from top model
    if m.modelId:
        card = hf_hub_download(repo_id=m.modelId, filename="README.md")
        print(f"Downloaded card for {m.modelId} at {card}")
        break
```

### Update Cadence

Monitor weekly via RSS/Webhook for new or updated models.

## ModelDB (MIT Computational Models Database)

Primarily computational neuroscience and ecological models in standardized archives.

### Access Methods

* OAI-PMH endpoint: Harvest metadata in Dublin Core format.
* Bulk tarballs: Download code archives per model.

### Example: Harvest Metadata via OAI-PMH

import requests
from xml.etree import ElementTree as ET

# Base OAI-PMH URL
base = "https://senselab.med.yale.edu/ModelDB/oai"
# List records
params = {'verb': 'ListRecords', 'metadataPrefix': 'oai_dc'}
resp = requests.get(base, params=params)
resp.raise_for_status()
root = ET.fromstring(resp.text)
for record in root.findall('.//{http://www.openarchives.org/OAI/2.0/}record'):
    identifier = record.find('.//{http://purl.org/dc/elements/1.1/}identifier').text
    title = record.find('.//{http://purl.org/dc/elements/1.1/}title').text
    print(f"ModelDB record: {identifier} - {title}")

### Update Cadence

Harvest monthly via OAI-PMH; large change cycles, so monthly is sufficient.

## JRC Data Catalogue (EU Environmental Models)

Includes workflow models for water balance, land-use change, climate impact assessments.

### Access Methods

* CKAN API: List and download dataset resources in JSON.
* Bulk exports: CKAN package_show and resource_download endpoints.

### Example: List JRC Model Resources

```python
import requests

base = "https://data.jrc.ec.europa.eu/api/3/action"
# Search for packages tagged 'model'
resp = requests.get(f"{base}/package_search", params={'q': 'model', 'rows': 20})
resp.raise_for_status()
results = resp.json()['result']['results']
for pkg in results:
    print(f"Dataset: {pkg['title']} ({pkg['name']})")
    for res in pkg['resources']:
        if res['format'] in ['ZIP', 'JSON', 'PY']:  # code archives or data
            print(f"  - Resource: {res['name']} ({res['format']}) -> {res['url']}")
```

### Update Cadence

CKAN catalog updates quarterly; schedule quarterly checks for new or updated model packages.

# Podcasts & YouTube Channels

## Podcasts

Need to identify these...

### Access Methods

* RSS/Atom feeds: Standard for episode metadata.
* PodcastIndex.org API: Centralized index with metadata and feed discovery.
* iTunes Search API: Alternative discovery via show lookup.

### Example: Fetch & Download Episodes (Python)

```python
import feedparser, requests, os

def harvest_podcast(feed_url, max_eps=5, out_dir='data/podcasts'):
    os.makedirs(out_dir, exist_ok=True)
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:max_eps]:
        audio_url = entry.enclosures[0].href
        title = entry.title.replace('/', '_')
        fname = f"{out_dir}/{title}.mp3"
        if not os.path.exists(fname):
            resp = requests.get(audio_url, stream=True)
            with open(fname, 'wb') as f:
                for chunk in resp.iter_content(1024): f.write(chunk)
            print(f"Downloaded: {entry.title}")

# Example: _Ecosystem Pulse_ feed
harvest_podcast('https://example.org/ecosystem-pulse/feed.xml', max_eps=3)
```

### Discovery & Bulk Harvest

* Use PodcastIndex endpoints to search by keyword (ecology, conservation).
* Bulk: ingest OPML lists or slice by category in iTunes API.

### Update Cadence

* Poll RSS feeds daily; notify on new entries.
* Re-index feed metadata weekly to catch licensing or category changes

## YouTube Channels

Videos under standard YouTube license; filter for Creative Commons–licensed content via API videoLicense=creativeCommon.

### Access Methods

* YouTube Data API v3: Query channels, playlists, and videos.
* yt-dlp (or youtube-dl): Bulk download audio/video files programmatically.

### Example: List & Download Channel Videos (Python)

```python
from googleapiclient.discovery import build
import os, subprocess

API_KEY = 'YOUR_API_KEY'
yt = build('youtube', 'v3', developerKey=API_KEY)
channel_id = 'UC12345_ecology'
# 1. Get uploads playlist
res = yt.channels().list(part='contentDetails', id=channel_id).execute()
upload_pl = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
# 2. List latest videos
videos = yt.playlistItems().list(playlistId=upload_pl, part='snippet', maxResults=5).execute()
for item in videos['items']:
    vid = item['snippet']['resourceId']['videoId']
    url = f'https://www.youtube.com/watch?v={vid}'
    # Download audio-only
    subprocess.run(['yt-dlp', '-x', '--audio-format', 'mp3', '-o', f'data/youtube/{vid}.%(ext)s', url])
    print(f"Downloaded video {vid}")
```

### Filtering & Multilingual

* Set videoSyndicated and videoLicense in API queries.
* Use captions.list endpoint to fetch auto-generated or community subtitles in various languages.

### Update Cadence

* Check channels weekly for new uploads.
* Refresh caption lists monthly to capture new languages.

# Libraries

## Library of Congress

Pre‑1927 works are Public Domain; later items often CC‑BY or marked rights‑protected.

### Access Methods

* REST API: Search item metadata and full‑text links via https://www.loc.gov/collections/ endpoints.
* IIIF Manifests: High‑res page images—manifest URLs under each item’s @id.

### Example: Fetch IIIF Manifest for an Item

```python
import requests, json

# Search for an item by subject
q = 'ecology'
url = f'https://www.loc.gov/collections/?fo=json&at=results&st=list&q={q}'
resp = requests.get(url)
resp.raise_for_status()
items = resp.json()['results']
# Grab first item's IIIF manifest
item = items[0]
manifest_url = item.get('image_url')
if manifest_url:
    manifest = requests.get(manifest_url + '/manifest.json').json()
    print(json.dumps(manifest, indent=2)[:500])
```

### Update Cadence

IIIF manifests and collection feeds update continuously; schedule weekly polling for new items.

## Bibliothèque nationale de France (BnF) – Gallica

Public Domain monographs; CC‑BY for modern digital editions.

### Access Methods

* OAI‑PMH: Endpoint at https://gallica.bnf.fr/oai delivering Dublin Core.
* IIIF: Manifests at https://gallica.bnf.fr/iiif/ per item.

### Example: Harvest Metadata via OAI‑PMH

```python
import requests
from xml.etree import ElementTree as ET
base = 'https://gallica.bnf.fr/oai'
params = {'verb':'ListRecords','metadataPrefix':'oai_dc','set':'books'}
resp = requests.get(base, params=params)
root = ET.fromstring(resp.text)
for rec in root.findall('.//{http://www.openarchives.org/OAI/2.0/}record'):
    title = rec.find('.//{http://purl.org/dc/elements/1.1/}title').text
    print(f"Title: {title}")
```

### Update Cadence

OAI‑PMH feeds update as items are digitized; schedule weekly harvest.

## National Library of Australia – Trove

Public Domain (pre‑1955); CC‑BY for newer content where indicated.

### Access Methods

* Trove REST API: https://api.trove.nla.gov.au/v2/result (requires free key).
* Bulk Data: Trove data dumps via NLA data feeds.

### Example: Search & Download Metadata

```
import requests
API_KEY = 'YOUR_TROVE_KEY'
params = {
    'q': 'ecology',
    'zone': 'book',
    'encoding': 'json',
    'key': API_KEY
}
resp = requests.get('https://api.trove.nla.gov.au/v2/result', params=params)
data = resp.json()
for rec in data['response']['zone'][0]['records']['work'][:5]:
    print(rec['title'], rec['identifier'])
```

### Update Cadence

Incremental harvest via daily API feeds; schedule daily metadata fetch and monthly full dumps.

## Deutsche Digitale Bibliothek (Germany)

Aggregates public‑domain and CC‑BY monographs from German institutions.

### Access Methods

* REST API & OAI‑PMH: https://api.deutsche-digitale-bibliothek.de supports both.
* IIIF: Manifests under item metadata.

### Example: List Items via API

```python
import requests
params = {'query': 'Ecologie', 'rows': 10}
resp = requests.get('https://api.deutsche-digitale-bibliothek.de/search/items', params=params)
items = resp.json()['items']
for it in items:
    print(it['title'], it['id'])
```

### Update Cadence

Metadata indexed weekly; schedule weekly API harvest.

## National Diet Library (Japan)

Public Domain (pre‑copyright) Japanese and Western works; rights stated in metadata.

### Access Methods

* SRU API: https://iss.ndl.go.jp/api/opensearch returns JSON‑LD.
* IIIF: Manifests available per record.

### Example: OpenSearch Query

```python
import requests
params = {'operation': 'searchRetrieve','query': 'integration ecology','recordSchema':'dcndl'}
resp = requests.get('https://iss.ndl.go.jp/api/opensearch', params=params)
print(resp.json())
```

### Update Cadence

Daily metadata updates; schedule daily polling.

## Europeana Collections (Pan‑EU)

Aggregates Public Domain, CC‑BY, and CC‑BY‑SA works from European libraries.

### Access Methods

* REST API: https://api.europeana.eu/record/v2/search.json (requires key).
* OAI‑PMH: Available at https://www.europeana.eu/api/oai/.
* IIIF: Many records expose IIIF manifests.

### Example: Search via Europeana API

```python
import requests
KEY = 'YOUR_EUROPEANA_KEY'
params = {'wskey': KEY, 'query': 'ecology', 'rows': 5}
resp = requests.get('https://api.europeana.eu/record/v2/search.json', params=params)
for obj in resp.json()['items']:
    print(obj['title'], obj['edmPreview'])
```

### Update Cadence

API incremental updates daily; OAI‑PMH metadata weekly.

##  Biblioteca Nacional de Brasil (BNB)

Public Domain: pre-20th-century works; CC-BY for modern editions.

### Access Methods

* OAI-PMH: https://hemerotecadigital.bn.gov.br/oai (Dublin Core)
* REST API: https://bndigital.bn.gov.br/api/v1/items for JSON metadata
* IIIF: Manifests at https://bndigital.bn.gov.br/iiif/{item_id}/manifest.json

### Example: OAI-PMH Harvest

```python
import requests
from xml.etree import ElementTree as ET

base = 'https://hemerotecadigital.bn.gov.br/oai'
params = {'verb': 'ListRecords', 'metadataPrefix': 'oai_dc', 'set': 'Monographs'}
resp = requests.get(base, params=params)
resp.raise_for_status()
root = ET.fromstring(resp.text)
for record in root.findall('.//{http://www.openarchives.org/OAI/2.0/}record'):
    title = record.find('.//{http://purl.org/dc/elements/1.1/}title').text
    print(f"Title: {title}")
```

### Update Cadence

Weekly OAI-PMH harvest; monthly IIIF manifest sync.

## Biblioteca Nacional de Chile – Memoria Chilena

Public Domain; rights statements in metadata.

### Access Methods

* REST API: https://www.memoriachilena.gob.cl/ws/catalogo?texto={query}&formato=json
* IIIF: Manifests at https://www.memoriachilena.gob.cl/iiif/{item_id}/manifest.json

### Example: API Query & Parse

```python
import requests

params = {'texto': 'ecologia', 'formato': 'json', 'pagina': 1}
resp = requests.get('https://www.memoriachilena.gob.cl/ws/catalogo', params=params)
resp.raise_for_status()
data = resp.json()
for item in data.get('coleccion', []):
    print(item['titulo'], item['id'])
```

### Update Cadence

Monthly API polling; on-demand IIIF harvesting.

## Biblioteca Nacional del Perú

Public Domain for most monographs; check metadata for exceptions.

### Access Methods

* SRU API: http://bdpi.cultura.gob.pe/sru?operation=searchRetrieve&version=1.1
* IIIF: https://bdpi.cultura.gob.pe/iiif/{pid}/manifest.json

### Example: SRU Harvest

```python
import requests
from xml.etree import ElementTree as ET

params = {
    'operation': 'searchRetrieve',
    'version': '1.1',
    'query': 'dc.subject=Ecología'
}
resp = requests.get('http://bdpi.cultura.gob.pe/sru', params=params)
resp.raise_for_status()
root = ET.fromstring(resp.text)
for rec in root.findall('.//record'):
    title = rec.find('.//{http://purl.org/dc/elements/1.1/}title').text
    print(f"Title: {title}")
```

### Update Cadence

Monthly SRU queries; quarterly IIIF checks.

## National Library of South Africa (NLSA)

Public Domain and CC-BY where indicated.

### Access Methods

* OAI-PMH: http://archive.nlsa.ac.za/oai/ (Dublin Core)
* IIIF: Manifests at http://iiif.nlsa.ac.za/{item_id}/manifest.json

### Example: OAI-PMH Harvest

```python
import requests
from xml.etree import ElementTree as ET

base = 'http://archive.nlsa.ac.za/oai/'
params = {'verb': 'ListRecords', 'metadataPrefix': 'oai_dc'}
resp = requests.get(base, params=params)
resp.raise_for_status()
root = ET.fromstring(resp.text)
for rec in root.findall('.//record'):
    title = rec.find('.//{http://purl.org/dc/elements/1.1/}title').text
    print(f"Title: {title}")
```

### Update Cadence

Weekly OAI-PMH harvest; monthly IIIF sync.

## Africa Digital Library (ADL)

Public Domain digitized monographs.

### Access Methods

* Bulk Export: https://www.africadigitallibrary.org/download/monographs.zip
* IIIF: Manifests at https://cdli.uwm.edu/iiif/{id}/manifest.json

### Example: Bulk Download

```python
import requests

url = 'https://www.africadigitallibrary.org/download/monographs.zip'
resp = requests.get(url)
with open('adl_monographs.zip', 'wb') as f:
    f.write(resp.content)
print("Downloaded ADL monographs archive")
```

### Update Cadence

Quarterly bulk export; quarterly IIIF manifest harvest.

## Digital Library Kenya (KU-KSL)

CC-BY and Public Domain collections.

### Access Methods

* DSpace REST API: https://digital.library.ku.ac.ke/rest/items
* OAI-PMH: https://digital.library.ku.ac.ke/oai/request

### Example: DSpace REST Harvest

```
import requests
resp = requests.get('https://digital.library.ku.ac.ke/rest/items?limit=5')
for item in resp.json().get('items', []):
    title = item['metadata'].get('dc.title', [{'value': None}])[0]['value']
    print(f"Title: {title}")
```

### Update Cadence

Weekly API polling; on-demand OAI-PMH.

## National Digital Library of India (NDLI)

Public Domain and CC-BY licensed resources.

### Access Methods

REST API: https://ndl.iitkgp.ac.in/api/v1/search?q={query}&format=json
OAI-PMH: https://ndl.iitkgp.ac.in/oai
IIIF: https://ndl.iitkgp.ac.in/iiif/{id}/manifest.json

### Example: REST API Query

```python
import requests

params = {'q': 'ecology', 'format': 'json', 'rows': 5}
resp = requests.get('https://ndl.iitkgp.ac.in/api/v1/search', params=params)
for doc in resp.json().get('resultList', []):
    print(doc.get('title'), doc.get('id'))
```

### Update Cadence

Daily metadata harvest; monthly IIIF sync.

## National Library of China (NLC)

Public Domain for ancient texts; check metadata for modern rights.

### Access Methods

* REST API: https://opac.nlc.cn/search?q={query}&format=json
* IIIF: https://opac.nlc.cn/iiif/{id}/info.json

### Example: Metadata Query

```python
import requests

resp = requests.get(
    'https://opac.nlc.cn/search',
    params={'q': '生态学', 'format': 'json'}
)
for item in resp.json().get('docs', [])[:5]:
    print(item.get('title'), item.get('recid'))
```

### Update Cadence

Monthly API polling; quarterly IIIF checks.

## National Library Board Singapore (NLB)

Public Domain and CC-BY for digital collections.

### Access Methods

* REST API: https://eresources.nlb.gov.sg/api/items?q={query}&limit=5
* IIIF: https://eresources.nlb.gov.sg/iiif/{id}/manifest.json

### Example: API Harvest

```python
import requests

resp = requests.get(
    'https://eresources.nlb.gov.sg/api/items',
    params={'q': 'ecology', 'limit': 5}
)
for itm in resp.json().get('items', []):
    print(f"Title: {itm.get('title')}, ID: {itm.get('id')}")
```

### Update Cadence

Weekly API polling; monthly IIIF sync.

## National Library of Korea (NLK)

Pre‑20th‑century works: Public Domain; modern digitizations often CC‑BY.

### Access Methods

* REST API: JSON metadata endpoints (e.g. search and item details).
* OAI‑PMH: via KORCIS at http://korcis.nl.go.kr/oai delivering Dublin Core.
* IIIF: Manifests under each item ID: https://www.nl.go.kr/iiif/{id}/manifest.json.

### Example: REST API Search & IIIF Fetch

```python
import requests

# 1. Search metadata
api_url = 'https://api.nl.go.kr/search'  # placeholder; replace with NLK API endpoint
params = {'query': 'ecology', 'format': 'json', 'rows': 5}
resp = requests.get(api_url, params=params)
resp.raise_for_status()
items = resp.json().get('docs', [])
for doc in items:
    item_id = doc['id']
    print('Title:', doc['title'])
    # 2. Fetch IIIF manifest
    manifest_url = f'https://www.nl.go.kr/iiif/{item_id}/manifest.json'
    mf = requests.get(manifest_url).json()
    print('IIIF canvases:', len(mf.get('sequences', [])[0].get('canvases', [])))
```

### Update Cadence

Poll REST and OAI‑PMH feeds weekly; IIIF manifests on-demand or monthly.

## National Institute of Ecology (NIE)

Hosts National Environment Survey occurrence data; CC0 on GBIF.

### Access Methods

* GBIF API: occurrences via datasetKey or publisher.
* DwC‑A Bulk: download full Darwin Core Archive.

### Example: GBIF Occurrence Download

```python
import requests

dataset_key = 'NIEK_NES_2024'  # example key
url = f'https://api.gbif.org/v1/occurrence/search?datasetKey={dataset_key}&limit=300'
resp = requests.get(url)
resp.raise_for_status()
records = resp.json().get('results', [])
print(f'Fetched {len(records)} NIE occurrence records')
```

### Update Cadence

Monitor GBIF registry monthly; full DwC‑A biennially after survey releases.

## National Institute of Biological Resources (NIBR)

Taxonomic checklists and occurrences; public domain or CC‑BY.

### Access Methods

* NIBR Portal API: species queries (Korean/English).
* GBIF API: filter by publisherKey for NIBR datasets.

### Example: GBIF Publisher Occurrences

```
import requests

publisher_key = 'https://www.gbif.org/publisher/6d2f6f'  # NIBR example
url = 'https://api.gbif.org/v1/occurrence/search'
params = {'publisher': publisher_key, 'limit': 200}
resp = requests.get(url, params=params)
print('NIBR records:', len(resp.json().get('results', [])))
```

### Update Cadence

Harvest monthly from GBIF; portal API weekly.

## EcoBank Platform

National ecological data integration platform; mixed license—confirm per dataset.

### Access Methods

* EcoBank REST API: authenticated JSON endpoints.
* Web interface bulk exports for select datasets.

### Example: EcoBank API Fetch

```
import requests

api_url = 'https://www.ecobank.kr/api/v1/data'  # placeholder
token = 'YOUR_API_TOKEN'
headers = {'Authorization': f'Bearer {token}'}
params = {'category': 'plot', 'limit': 100}
resp = requests.get(api_url, headers=headers, params=params)
print('EcoBank items:', len(resp.json().get('data', [])))
```

### Update Cadence

Sync weekly; check for new datasets monthly.

## Korea Open Government Data Portal (Data.go.kr)

Aggregates environment-related datasets under Open Government Data Act (CC‑BY/public domain).

### Access Methods

* REST API: requires service key; JSON/XML responses.
* Bulk CSV/XML downloads via data catalog.

### Example: API Query

```python
import requests

service_key = 'YOUR_SERVICE_KEY'
api_url = 'https://api.data.go.kr/openapi/tn_pubr_public_manage_api'  # example
params = {
    'serviceKey': service_key,
    'type': 'json',
    'numOfRows': 50,
    'pageNo': 1,
    'organCd': '1120000',  # Ministry of Environment
}
resp = requests.get(api_url, params=params)
resp.raise_for_status()
print('Records:', resp.json().get('response', {}).get('body', {}).get('items', []))
```

### Update Cadence

High-frequency feeds daily; static datasets monthly.

## Korea Meteorological Administration (KMA)

Weather and climate data public domain under KMA policy.

### Access Methods

* KMA Open API: station observations, forecasts, air quality.
* Bulk CSV/XML: via OpenMET Data Portal.

### Example: Current Weather Fetch

```python
import requests

api_key = 'YOUR_KMA_KEY'
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params = {
    'serviceKey': api_key,
    'pageNo': 1,
    'numOfRows': 100,
    'dataType': 'JSON',
    'base_date': '20250701',
    'base_time': '0600',
    'nx': 60,
    'ny': 127,
}
resp = requests.get(url, params=params)
data = resp.json()
print(data['response']['body']['items']['item'][:5])
```

### Update Cadence

Hourly for real‑time; daily for summary products.

## National Forest Inventory (KFS & NIFoS)

Plot‑level forest attributes; CC‑BY/public domain (verify per release).

### Access Methods

* NIFoS Portal Downloads: shapefiles/CSV on request or via research repository.
* Published CSVs: HTTP bulk from KFS GitHub or data portal.

### Example: CSV Download

```python
import requests

url = 'https://github.com/kfs-nifos/nfi-data/raw/main/nfi_plots.csv'
resp = requests.get(url)
with open('nfi_plots.csv', 'wb') as f:
    f.write(resp.content)
print('Downloaded NFI plot data')
```

### Update Cadence

Every 5 years with main survey; interim updates as released.