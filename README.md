# Integral Ecology Library Demo

A containerized proof-of-concept for an open-access Integral Ecology digital library, featuring:

* **Static Frontend**: Searchable list of OA resources (HTML, PDF, podcasts, datasets).
* **ETL Pipeline**: Celery-based jobs for harvesting OAI-PMH feeds and RSS/podcast PDFs, text extraction via Apache Tika.
* **Backend API**: FastAPI service with PostgreSQL for metadata storage and retrieval.
* **DevOps**: Docker Compose for local orchestration; GitHub Actions for CI/CD.
* **Monitoring & Logging**: Prometheus, cAdvisor, Grafana for metrics; Loki/Promtail for logs.

---

## 🔧 Prerequisites

* **Docker** (>= 20.10) & **Docker Compose** (>= 1.29)
* **Git** (for code checkout)
* **Python 3.9+** (optional, for local ETL/API development and testing)
* **Environment file**: Copy `.env.example` to `.env` and set:

  ```bash
  DB_USER=user
  DB_PASSWORD=pass
  DB_NAME=library
  S3_BUCKET=integral-ecology-bucket
  DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
  ```

---

## 📁 Project Structure

```text
.
├── demo_site/                # Static HTML/CSS/JS frontend demo
├── etl/                      # ETL scripts and dependencies
│   ├── etl_tasks.py         # Celery tasks for harvesting & parsing
│   └── requirements.txt     # Python dependencies for ETL
├── api/                      # Backend service (FastAPI + SQLAlchemy)
│   ├── Dockerfile
│   ├── requirements.txt     # Python dependencies for API
│   └── main.py              # FastAPI application code
├── monitoring/               # Monitoring & logging configs
│   ├── prometheus.yml
│   ├── loki-config.yaml
│   └── promtail-config.yaml
├── terraform/                # IaC for AWS (EKS, RDS, S3)
├── k8s/                      # Kubernetes manifests for services
├── .env.example              # Example environment variables
├── .github/                  # CI/CD workflows
│   └── workflows/ci-cd.yml
├── docker-compose.yml        # Core infrastructure definition
└── README.md                 # This file
```

---

## 🚀 Getting Started

1. **Clone the repo**:

   ```bash
   git clone https://github.com/your-org/integral-ecology-demo.git
   cd integral-ecology-demo
   ```

2. **Configure environment**:

   ```bash
   cp .env.example .env
   # Edit .env with your DB and bucket settings
   ```

3. **Start all services**:

   ```bash
   docker-compose up -d
   ```

4. **Access components**:

   * Frontend: [http://localhost:8080](http://localhost:8080)
   * API: [http://localhost:8000](http://localhost:8000)
   * API Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   * RabbitMQ UI: [http://localhost:15672](http://localhost:15672)  (guest/guest)
   * Prometheus: [http://localhost:9090](http://localhost:9090)
   * Grafana:    [http://localhost:3000](http://localhost:3000)  (admin/admin)
   * cAdvisor:   [http://localhost:8081](http://localhost:8081)

5. **Run only the API service**:

   ```bash
   docker-compose up api
   ```

6. **Run ETL locally** (without Docker):

   ```bash
   cd etl
   pip install -r requirements.txt
   celery -A etl_tasks worker --loglevel=info
   ```

---

## 🔄 ETL Pipeline

* **OAI-PMH Harvest**: Daily at 02:00 UTC (configurable) via `harvest_oai` task.
* **RSS/Podcast Harvest**: Daily at 03:00 UTC via `harvest_rss` task.
* **Text Extraction**: Apache Tika for PDF → plain text, stored in S3 bucket.

Configuration variables (via `.env`):

```env
S3_BUCKET=integral-ecology-bucket
DATABASE_URL=postgresql://user:pass@db:5432/library
```

---

## 🛠 CI/CD with GitHub Actions

* **Lint & Test**: Flake8 + pytest for ETL and API code.
* **Build**: `docker-compose build` for all services.
* **Deploy**: SSH to remote server; pull and rebuild on `main` branch using secrets `SSH_HOST`, `SSH_USER`, `SSH_KEY`.

---

## 📊 Monitoring & Logging

* **Prometheus**: Scrapes metrics from Prometheus itself and cAdvisor.
* **Grafana**: Dashboards for container metrics + logs.
* **Loki & Promtail**: Aggregates system & application logs.

See `/monitoring` for configuration files.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/name`.
3. Commit changes: `git commit -m "feat: description"`.
4. Push: `git push origin feature/name`.
5. Open a Pull Request against `main`.

Please adhere to existing code style and include tests for new features.

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE.md](LICENSE.md) for details.
