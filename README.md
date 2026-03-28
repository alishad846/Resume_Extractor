# Resume AI Platform

Enterprise-ready resume intelligence that blends FastAPI/Celery microservices, SpaCy/BERT/FAISS NLP, Streamlit + optional React dashboards, and Dockerized infrastructure to extract, score, match, and analyze resumes in production.

## Features
- **Entity-rich resume extraction** – SpaCy + transformer pipelines capture contacts, skills, experience, education, certifications, projects, and achievements.
- **Multi-dimensional scoring** – Weighted metrics for skills, experience, education, projects, and completeness generate actionable scores plus AI feedback.
- **Semantic JD matching** – FAISS + BERT embeddings compare resumes with job descriptions, detect gaps, and power similarity search.
- **Recruiter analytics** – Batch parsing, Redis-powered filters, career dashboards, and MinIO-backed storage streamline candidate review.
- **Production readiness** – FastAPI APIs, PostgreSQL, Celery, Redis cache, Docker Compose orchestration, and Kubernetes manifests support secure scaling and CI/CD.

## What It Does
- **Candidate intelligence** – Upload resumes through Streamlit, run extraction, receive AI coaching, and view scoring vs. JD/learning paths.
- **Recruiter automation** – Parse/score hundreds of resumes, search semantically, monitor KPIs, and manage candidate pools.
- **Platform operations** – FastAPI endpoints, Celery workers, Redis cache, PostgreSQL, and FAISS similarity search deliver scalable deployments with observability hooks.

## Technology Stack
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, Celery, Redis, Alembic migrations
- **NLP/ML:** SpaCy, HuggingFace Transformers, Sentence-Transformers, FAISS, scikit-learn, NLTK
- **Frontend:** Streamlit candidate portal, optional React recruiter interface, Plotly visualizations
- **Infra:** Docker, Docker Compose, Kubernetes manifests, GitHub Actions, AWS/GCP/Azure deployment scripts

## Installation & Setup
### Prerequisites
- Python 3.10+ (matching backend `requirements.txt`)
- Docker & Docker Compose for containerized development or production images
- PostgreSQL 12+, Redis, and optional MinIO/S3 storage (run via Docker if needed)
- CLI tools: `git`, `python -m venv`, `pip`, `streamlit`, `locust`

### Backend (Windows example)
```bash
cd backend
python -m venv venv
.\\venv\\Scripts\\activate
pip install -r requirements.txt
python -c "import spacy; spacy.cli.download('en_core_web_lg')"
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend/candidate-portal
python -m venv venv
.\\venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Full Stack via Docker Compose
```bash
docker-compose up -d
docker-compose logs -f
```
Use `docker-compose exec backend alembic upgrade head` for migrations and `docker-compose exec backend pytest` for tests when the stack is running.

## Deployment Paths
- **Docker Compose:** Build backend/frontend images, then run `docker-compose up -d` (backend `:8000`, frontend `:8501`).
- **AWS/EKS:** Push images to ECR, deploy Kubernetes manifests in `k8s/`, and attach managed PostgreSQL/Redis resources.
- **Heroku:** Create `resume-ai-backend` & `resume-ai-frontend`, push `main`, and configure required environment variables through the dashboard.

## Testing & Quality
- Unit tests: `pytest backend/tests/ -v`
- Integration tests: `pytest backend/tests/test_api.py -v`
- Coverage reports: `pytest --cov=app backend/tests/`
- Load testing: `locust -f load_tests.py -u 1000 -r 100`
- CI/CD workflows rely on GitHub Actions defined for linting, container builds, and tests.

## Documentation & References
- System diagrams/architecture: `ARCHITECTURE.md`
- Implementation guides: `IMPLEMENTATION_GUIDE.md`
- Delivery summary: `DELIVERY_SUMMARY.md`
- Deployment instructions: `DEPLOYMENT_GUIDE.md`
- API & user manuals: `docs/API.md`, `docs/USER_GUIDE.md`, `docs/DEVELOPMENT.md`
- Production deep dives: `README_PRODUCTION.md`

## Project Layout
```
resume-ai-platform/
├── backend/               # FastAPI + Celery + database models/tests
├── frontend/
│   ├── candidate-portal/  # Streamlit application
│   └── recruiter-dashboard/# React dashboard (optional)
├── components/            # Shared UI/UX helpers
├── pages/                 # Streamlit/React page definitions
├── utils/                 # Helper scripts and utilities
├── data/                  # Sample datasets and seeds
├── docs/                  # Supporting documentation
├── __pycache__/           # Auto-generated cache
├── app.py                 # Entry points or automation wrappers
├── requirements.txt       # Top-level dependencies
├── DEPLOYMENT_GUIDE.md
├── README_PRODUCTION.md
└── ARCHITECTURE.md
```

## Contributing
1. Fork the repository, create a `feature/<name>` branch, and keep commits focused.
2. Update or add README/implementation notes if behavior changes.
3. Run relevant tests (`pytest`, `streamlit`, CLI checks) and mention coverage impacts.
4. Push to your branch and open a PR describing the change, linked tests, and deployment implications.

## Support
- Email: support@resumeai.com
- Issues: GitHub Issues (reference `README_PRODUCTION.md`)
- Docs: check `docs/` and `/api/docs` once the backend is running locally.

## License
MIT. See `LICENSE` for details.
