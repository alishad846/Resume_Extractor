# Resume AI Platform - Production Architecture

## 📋 System Overview

A comprehensive AI-powered resume processing and ATS (Applicant Tracking System) platform with recruitment analytics, resume scoring, and JD matching capabilities.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
├──────────────────────┬──────────────────────────────────────┤
│  Candidate Portal    │      Recruiter Dashboard             │
│  (Streamlit)         │      (React/Streamlit)               │
│  - Upload Resume     │      - View Candidates               │
│  - Get Feedback      │      - Filter & Search               │
│  - Score Tracking    │      - JD Matching                   │
└──────────────────────┴──────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                    API GATEWAY (FastAPI)                      │
├──────────────────────────────────────────────────────────────┤
│  • Authentication & Authorization                            │
│  • Rate Limiting & Caching                                   │
│  • Request Validation & Error Handling                       │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                   MICROSERVICES LAYER                        │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Resume       │ NLP &        │ Scoring &    │ Analytics &    │
│ Processing   │ Extraction   │ Ranking      │ Insights       │
│ Service      │ Service      │ Service      │ Service        │
└──────────────┴──────────────┴──────────────┴────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                  DATA PROCESSING LAYER                       │
├───────────────┬──────────────┬──────────────────────────────┤
│ PDF/DOC       │ SpaCy NER    │ BERT Embeddings &            │
│ Extraction    │ SpaCy        │ Semantic Search (FAISS)      │
│               │ Transformers │                              │
└───────────────┴──────────────┴──────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                    PERSISTENCE LAYER                         │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ PostgreSQL   │ Redis Cache  │ FAISS Index  │ MinIO (Files)  │
│ (Metadata,   │ (Session,    │ (Embeddings) │ (Resume PDFs)  │
│ Users, JDs)  │ Tokens)      │              │                │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

---

## 🔧 Tech Stack

### Backend

- **Framework**: FastAPI (async, high-performance)
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL (primary), Redis (caching)
- **Authentication**: JWT + OAuth2
- **API Documentation**: OpenAPI/Swagger

### NLP & ML

- **NER**: SpaCy (en_core_web_lg)
- **Transformers**: HuggingFace BERT, DistilBERT
- **Embeddings**: Sentence-Transformers
- **Semantic Search**: FAISS
- **Text Processing**: NLTK, Regex patterns

### Frontend

- **Candidate Portal**: Streamlit (Python)
- **Recruiter Dashboard**: React + TypeScript (optional) or Streamlit
- **UI Components**: Custom CSS, Chart.js/Plotly for analytics

### Infrastructure

- **Container**: Docker & Docker Compose
- **Storage**: MinIO (S3-compatible)
- **Queue**: Celery + Redis (async task processing)
- **Monitoring**: Prometheus, Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

---

## 📁 Folder Structure

```
resume-ai-platform/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry
│   │   ├── config.py               # Configuration
│   │   ├── security.py             # JWT, OAuth2
│   │   ├── database.py             # DB connection
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # Auth endpoints
│   │   │   ├── resumes.py          # Resume upload/get
│   │   │   ├── extraction.py       # Entity extraction
│   │   │   ├── scoring.py          # Resume scoring
│   │   │   ├── search.py           # Semantic search
│   │   │   └── analytics.py        # Analytics endpoint
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # User model
│   │   │   ├── resume.py           # Resume model
│   │   │   ├── job_description.py  # JD model
│   │   │   ├── extraction.py       # Extracted data model
│   │   │   └── feedback.py         # AI feedback model
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── job_description.py
│   │   │   └── feedback.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── resume_processor.py # PDF extraction
│   │   │   ├── nlp_extractor.py    # NER extraction
│   │   │   ├── scorer.py           # Scoring engine
│   │   │   ├── embeddings.py       # Embeddings gen
│   │   │   ├── semantic_search.py  # FAISS search
│   │   │   ├── recommendations.py  # AI suggestions
│   │   │   └── analytics.py        # Analytics calc
│   │   │
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   ├── resume_processing.py # Celery tasks
│   │   │   └── embedding_generation.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── validators.py
│   │       ├── constants.py
│   │       └── helpers.py
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_resumes.py
│   │   └── test_services.py
│   │
│   ├── migrations/
│   │   └── alembic/
│   │
│   ├── requirements.txt
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── candidate-portal/           # Streamlit app
│   │   ├── pages/
│   │   │   ├── 1_home.py
│   │   │   ├── 2_upload_resume.py
│   │   │   ├── 3_resume_analysis.py
│   │   │   ├── 4_ai_feedback.py
│   │   │   └── 5_career_insights.py
│   │   │
│   │   ├── components/
│   │   │   ├── header.py
│   │   │   ├── sidebar.py
│   │   │   ├── charts.py
│   │   │   └── modals.py
│   │   │
│   │   ├── utils/
│   │   │   ├── api_client.py
│   │   │   └── constants.py
│   │   │
│   │   ├── streamlit_app.py
│   │   ├── requirements.txt
│   │   └── .streamlit/config.toml
│   │
│   └── recruiter-dashboard/        # React or Streamlit
│       ├── pages/
│       │   ├── 1_dashboard.py
│       │   ├── 2_candidates.py
│       │   ├── 3_jd_management.py
│       │   ├── 4_matching.py
│       │   └── 5_analytics.py
│       │
│       ├── components/
│       └── streamlit_app.py
│
├── models/
│   ├── spacy/
│   │   └── en_core_web_lg/         # SpaCy models
│   │
│   ├── bert/
│   │   ├── tokenizer/
│   │   └── model/
│   │
│   └── faiss/
│       └── resume_embeddings.index # FAISS index
│
├── data/
│   ├── sample_resumes/
│   ├── sample_jds/
│   ├── training_datasets/
│   └── embeddings_cache/
│
├── docs/
│   ├── API.md                      # API documentation
│   ├── DEPLOYMENT.md               # Deployment guide
│   ├── USER_GUIDE.md               # User guide
│   └── ARCHITECTURE.md             # This file
│
├── scripts/
│   ├── setup.sh                    # Setup script
│   ├── train_models.py             # Model training
│   └── migrate_db.sh               # DB migration
│
├── docker-compose.yml              # Multi-container setup
├── .dockerignore
├── .gitignore
├── .env.example
└── README.md
```

---

## 🎯 Core Features

### 1️⃣ Resume Processing & Extraction

- **PDF/DOC parsing** with error handling
- **Advanced NER** (SpaCy + BERT)
  - Name, Email, Phone, LinkedIn, GitHub
  - Skills, Certifications
  - Education, Degree, University
  - Experience, Company, Position, Duration
  - Projects, Languages, Tools
- **Data validation & normalization**
- **Duplicate detection**

### 2️⃣ Resume Scoring & Ranking

- **Multi-dimensional scoring**:
  - Skills match with JD (cosine similarity)
  - Experience relevance (years, level)
  - Education alignment
  - Project quality assessment
  - Keyword match percentage
- **Overall score**: 0-100 (weighted)
- **Ranking pipeline** for batch processing

### 3️⃣ JD Matching & Semantic Search

- **Job Description parsing** (skills, requirements, nice-to-haves)
- **Semantic matching** using FAISS + embeddings
- **Find similar resumes** in the database
- **Real-time search** with caching

### 4️⃣ AI-Powered Insights

- **Resume Quality Assessment**:
  - Completeness score
  - Clarity & readability score
  - ATS optimization tips
- **AI Improvement Suggestions**:
  - Missing sections
  - Weak bullet points
  - Skill gaps vs JD
  - Formatting recommendations
- **Job Role Prediction**:
  - ML-based role classification
  - Confidence scores

### 5️⃣ Recruiter Dashboard

- **Candidate Management**:
  - View all uploaded resumes
  - Filter by skills, experience, location
  - Search with intelligent ranking
- **JD Management**:
  - Upload/manage job descriptions
  - Auto-extract requirements
- **Matching Engine**:
  - Match JD against resume pool
  - View match scores with explanations
  - Shortlist candidates
- **Analytics & Insights**:
  - Skills distribution charts
  - Experience level distribution
  - Top candidates by score
  - Hiring funnel metrics

### 6️⃣ Candidate Portal

- **Resume Upload & Management**:
  - Upload resume
  - View extracted information
  - Edit/verify data
- **AI Feedback**:
  - Real-time quality assessment
  - Improvement suggestions
  - ATS optimization tips
- **Career Insights**:
  - Recommended skills to learn
  - Similar job roles
  - Salary insights (optional)
  - Career path recommendations

### 7️⃣ Authentication & Authorization

- **User types**: Admin, Recruiter, Candidate
- **JWT-based authentication**
- **Role-based access control** (RBAC)
- **OAuth2 integration** (Google, LinkedIn)

### 8️⃣ Analytics & Reporting

- **Real-time dashboards**
- **Charts & visualizations**:
  - Skills distribution
  - Experience vs Role matrix
  - Hiring metrics
  - Time-to-hire analytics
- **Export capabilities** (PDF, CSV)

---

## 🚀 API Endpoints Overview

### Authentication

- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - Logout

### Resume Management

- `POST /api/resumes/upload` - Upload resume
- `GET /api/resumes/{resume_id}` - Get resume details
- `GET /api/resumes` - List all resumes (paginated)
- `DELETE /api/resumes/{resume_id}` - Delete resume

### NLP Extraction

- `POST /api/extraction/extract` - Extract entities
- `GET /api/extraction/{resume_id}` - Get extracted data

### Scoring

- `POST /api/scoring/score-resume` - Score single resume
- `POST /api/scoring/batch-score` - Batch scoring
- `POST /api/scoring/score-with-jd` - Score against JD

### Semantic Search

- `POST /api/search/semantic` - Semantic search
- `GET /api/search/similar/{resume_id}` - Find similar

### AI Feedback

- `GET /api/feedback/{resume_id}` - Get AI suggestions
- `GET /api/feedback/improvement-tips/{resume_id}` - Improvement tips
- `POST /api/feedback/predict-role` - Job role prediction

### Job Descriptions

- `POST /api/jd/upload` - Upload JD
- `GET /api/jd/{jd_id}` - Get JD details
- `POST /api/jd/parse` - Parse JD

### Analytics

- `GET /api/analytics/dashboard` - Dashboard metrics
- `GET /api/analytics/skills-distribution` - Skills chart
- `GET /api/analytics/experience-distribution` - Experience chart
- `GET /api/analytics/hiring-funnel` - Hiring metrics

---

## 💾 Database Schema

### Users Table

```sql
users (
  id, username, email, password_hash, user_type,
  oauth_provider, oauth_id, created_at, updated_at
)
```

### Resumes Table

```sql
resumes (
  id, user_id, filename, file_path, file_size,
  extracted_text, upload_date, processing_status,
  overall_score, created_at, updated_at
)
```

### Extracted Data Table

```sql
extracted_data (
  id, resume_id, name, email, phone, linkedin,
  github, skills[], education[], experience[],
  projects[], languages[], certifications[],
  extracted_at
)
```

### Job Descriptions Table

```sql
job_descriptions (
  id, company_id, title, description, requirements[],
  nice_to_haves[], skills_required[], created_at
)
```

### Scoring Table

```sql
scores (
  id, resume_id, jd_id, skills_match, experience_score,
  education_score, overall_score, details{},
  calculated_at
)
```

---

## 🎨 UI/UX Design Highlights

### Candidate Portal

1. **Landing Page** - Hero section with CTA
2. **Upload Page** - Drag-drop resume upload with progress
3. **Analysis Page** - Side-by-side extracted data view
4. **Feedback Page** - AI suggestions with interactive tips
5. **Insights Page** - Career recommendations and stats

### Recruiter Dashboard

1. **Dashboard Home** - KPIs, recent activity
2. **Candidates List** - Filterable, sortable table
3. **JD Management** - Upload and manage job descriptions
4. **Matching Engine** - Real-time matching visualization
5. **Analytics** - Charts, metrics, export options

---

## 🔐 Security Considerations

- Environment variables for sensitive data
- Password hashing (bcrypt)
- JWT token expiration
- CORS configuration
- Rate limiting on API endpoints
- Input validation and sanitization
- Secure file upload (virus scanning)
- Data encryption at rest

---

## 📊 Performance Metrics

- Resume processing: < 5 seconds
- API response time: < 500ms
- Search query: < 100ms
- Concurrent users support: 1000+
- Database query optimization with indexing
- Caching strategy (Redis)
- Batch processing with Celery

---

## 🚢 Deployment

- **Docker containerization**
- **Kubernetes orchestration** (optional)
- **CI/CD pipeline** (GitHub Actions, GitLab CI)
- **Cloud deployment** (AWS, GCP, Azure)
- **Load balancing** (Nginx, HAProxy)
- **Auto-scaling** capabilities

---

## 📈 Future Enhancements

1. **Video Resume Analysis** - Extract insights from video
2. **Skill Assessment Tests** - Validate candidate skills
3. **Interview Scheduling** - Auto-scheduling integration
4. **Background Check Integration** - Third-party API
5. **Salary Prediction** - Based on profile
6. **Market Intelligence** - Competitive analysis
7. **Bulk Import** - CSV/bulk resume import
8. **Referral Program** - Employee referral tracking
9. **Mobile App** - Native mobile application
10. **Multi-language Support** - Global platform
