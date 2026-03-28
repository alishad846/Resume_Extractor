# Resume AI Platform - Complete Production Setup

## 🚀 Quick Start Guide

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLP models
python -c "import spacy; spacy.cli.download('en_core_web_lg')"

# 5. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 6. Run database migrations
alembic upgrade head

# 7. Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend/candidate-portal

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Streamlit app
streamlit run streamlit_app.py
```

### Docker Setup (Recommended)

```bash
# 1. Build and run all services
docker-compose up -d

# 2. Access services:
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/api/docs
# - Frontend: http://localhost:8501
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

---

## 📊 Feature Breakdown

### Phase 1: Foundation (Weeks 1-2)

- ✅ Basic PDF/resume extraction
- ✅ Regex-based NER
- ✅ Simple scoring system
- ✅ FastAPI backend structure

### Phase 2: Advanced NLP (Weeks 3-4)

- [ ] SpaCy NER integration
- [ ] BERT-based embeddings
- [ ] FAISS semantic search
- [ ] Advanced skill extraction

### Phase 3: Scoring & Matching (Weeks 5-6)

- [ ] Multi-dimensional scoring
- [ ] JD matching engine
- [ ] Resume ranking system
- [ ] Similarity calculations

### Phase 4: User Features (Weeks 7-8)

- [ ] User authentication (JWT/OAuth)
- [ ] Resume upload & storage
- [ ] AI feedback generation
- [ ] Career insights

### Phase 5: Recruiter Features (Weeks 9-10)

- [ ] Recruiter dashboard
- [ ] Batch processing
- [ ] Advanced filtering
- [ ] Analytics & reporting

### Phase 6: Polish & Deploy (Weeks 11-12)

- [ ] UI/UX refinement
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Production deployment

---

## 🏗️ System Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│            Load Balancer (Nginx/HAProxy)           │
└──────────────┬──────────────────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼──┐  ┌────▼───┐  ┌───▼──┐
│  API │  │  API   │  │ API  │
│ Pod1 │  │ Pod2   │  │ Pod3 │
└──────┘  └────────┘  └──────┘
    │          │          │
    └──────────┼──────────┘
               │
    ┌──────────┼──────────────┐
    │          │              │
 ┌──▼──┐  ┌────▼────┐    ┌────▼────┐
 │ DB  │  │  Cache  │    │ Storage  │
 │  PG │  │ Redis   │    │ MinIO    │
 └─────┘  └─────────┘    └──────────┘
```

---

## 🔐 Security Checklist

- [ ] Environment variables for secrets
- [ ] JWT token validation
- [ ] Input sanitization
- [ ] Rate limiting on APIs
- [ ] CORS configuration
- [ ] SQL injection prevention
- [ ] File upload validation
- [ ] Password hashing (bcrypt)
- [ ] API authentication (OAuth2)
- [ ] Data encryption at rest

---

## 📈 Performance Optimization

### Caching Strategy

- **Redis Cache**: User sessions, API responses
- **Query Caching**: Frequently accessed data
- **Full-page Cache**: Dashboard metrics

### Database Optimization

- **Indexing**: On user_id, status, created_at
- **Query Optimization**: Use appropriate JOINs
- **Connection Pooling**: PgBouncer for PostgreSQL

### API Optimization

- **Pagination**: Limit results to 50 items
- **Compression**: Gzip responses
- **Async Processing**: Celery for long tasks
- **CDN**: CloudFront for static assets

---

## 🧪 Testing Strategy

### Unit Tests

```bash
pytest backend/tests/test_services.py -v
```

### Integration Tests

```bash
pytest backend/tests/test_api.py -v
```

### Load Testing

```bash
locust -f load_tests.py -u 1000 -r 100
```

---

## 📦 Deployment

### AWS Deployment

```bash
# 1. Build Docker images
docker build -t resume-ai-backend:latest backend/
docker build -t resume-ai-frontend:latest frontend/

# 2. Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin ...
docker tag resume-ai-backend:latest ...amazonaws.com/resume-ai-backend:latest
docker push ...

# 3. Deploy to ECS/EKS
kubectl apply -f k8s/deployment.yaml
```

### Heroku Deployment

```bash
# 1. Create Heroku apps
heroku create resume-ai-backend
heroku create resume-ai-frontend

# 2. Deploy
git push heroku main
```

---

## 📚 API Documentation

Visit `http://localhost:8000/api/docs` for interactive API documentation

### Key Endpoints

**Authentication:**

- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login

**Resume Operations:**

- `POST /api/resumes/upload` - Upload resume
- `GET /api/resumes/{id}` - Get resume details
- `POST /api/extraction/extract` - Extract entities

**Scoring:**

- `POST /api/scoring/score-resume` - Score single resume
- `POST /api/scoring/batch-score` - Score multiple
- `POST /api/scoring/score-with-jd` - Score vs JD

**Search:**

- `POST /api/search/semantic` - Semantic search
- `GET /api/search/similar/{id}` - Find similar

**Analytics:**

- `GET /api/analytics/dashboard` - Dashboard metrics
- `GET /api/analytics/skills-distribution` - Skills chart
- `GET /api/analytics/hiring-funnel` - Hiring metrics

---

## 🛠️ Development Tips

### Local Development Setup

1. Use `docker-compose up` for full stack
2. Backend auto-reloads on file changes
3. Frontend hot-reloads with Streamlit
4. Access logs via `docker logs -f container_name`

### Database Management

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Common Issues & Solutions

**PostgreSQL Connection Error:**

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Reset database
docker exec postgres_container psql -U user -d resume_ai -c "DROP SCHEMA public CASCADE;"
```

**Memory Issues:**

```bash
# Increase Docker memory
# Edit Docker Desktop settings or docker-compose: mem_limit: 4g
```

---

## 📞 Support & Resources

- **Documentation**: `/docs` folder
- **API Reference**: `http://localhost:8000/api/docs`
- **Issue Tracker**: GitHub Issues
- **Email Support**: support@resumeai.com

---

## 📊 Production Checklist

- [ ] All tests passing (100% coverage)
- [ ] Security audit completed
- [ ] Performance benchmarks met
- [ ] Load testing passed (1000+ concurrent users)
- [ ] Disaster recovery plan
- [ ] Monitoring & alerts setup
- [ ] Documentation complete
- [ ] CI/CD pipeline configured
- [ ] SSL/TLS certificates
- [ ] Backup strategy defined
