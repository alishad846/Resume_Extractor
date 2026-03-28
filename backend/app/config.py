"""Application configuration settings."""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # App Configuration
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "*"]
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "http://127.0.0.1:3000",
    ]
    
    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/resume_ai_db"
    )
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_CACHE_EXPIRY: int = 3600  # 1 hour
    
    # File Storage Configuration (MinIO)
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET: str = "resumes"
    MINIO_USE_SSL: bool = False
    
    # File Upload Configuration
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_MIME_TYPES: List[str] = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    UPLOAD_TEMP_DIR: str = "/tmp/resume_uploads"
    
    # NLP Models Configuration
    SPACY_MODEL: str = "en_core_web_lg"
    BERT_MODEL: str = "bert-base-uncased"
    EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"
    
    # FAISS Configuration
    FAISS_INDEX_PATH: str = "./models/faiss/resume_embeddings.index"
    EMBEDDING_DIMENSION: int = 768
    
    # Celery Configuration
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Batch Processing
    BATCH_SIZE: int = 32
    WORKER_THREADS: int = 4
    
    # API Configuration
    API_VERSION: str = "1.0.0"
    API_RATE_LIMIT: int = 100  # requests per minute
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Initialize settings
settings = Settings()
