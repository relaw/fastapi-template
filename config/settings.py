"""
Application Settings

Configuration management using Pydantic Settings.
Loads environment variables from .env file.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Application
    APP_NAME: str = "Biznesplan Generator"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Database (PostgreSQL)
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False  # Set to True for SQL query logging
    
    # Redis (Celery broker + cache)
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_CEIDG: int = 259200  # 72 hours (3 days)
    CACHE_TTL_RESEARCH: int = 604800  # 7 days
    
    # API Keys - External Services
    CEIDG_API_KEY: str
    PODIO_APP_ID: str
    PODIO_APP_TOKEN: str
    PODIO_WORKSPACE_ID: str
    PODIO_CLIENT_ID: Optional[str] = None  # Global Podio OAuth (optional)
    PODIO_SECRET_KEY: Optional[str] = None  # Global Podio OAuth (optional)
    ANTHROPIC_API_KEY: str
    PERPLEXITY_API_KEY: Optional[str] = None  # Optional for MVP
    
    # Celery Configuration
    CELERY_BROKER_URL: Optional[str] = None  # Defaults to REDIS_URL
    CELERY_RESULT_BACKEND: Optional[str] = None  # Defaults to REDIS_URL
    CELERY_TASK_TIME_LIMIT: int = 1800  # 30 minutes max per task
    CELERY_TASK_SOFT_TIME_LIMIT: int = 1500  # 25 minutes soft limit
    
    # LLM Configuration (Anthropic Claude)
    LLM_MODEL: str = "claude-sonnet-4-5-20241022"
    LLM_MAX_TOKENS: int = 8000  # Max tokens per API call
    LLM_TEMPERATURE: float = 0.7
    LLM_TIMEOUT: int = 60  # API call timeout (seconds)
    LLM_MAX_RETRIES: int = 3
    
    # Cost Thresholds (USD)
    COST_ALERT_DAILY: float = 5.0  # Alert if daily cost exceeds this
    COST_ALERT_PER_PLAN: float = 0.50  # Alert if single plan costs more
    COST_TARGET_PER_PLAN: float = 0.30  # Target cost per biznesplan
    
    # Prompt Caching
    PROMPT_CACHE_TTL: int = 300  # 5 minutes (Anthropic default)
    PROMPT_CACHE_HIT_RATE_TARGET: float = 0.80  # Target 80% cache hit rate
    
    # Business Plan Generation
    BIZNESPLAN_TARGET_PAGES: int = 27  # Target: 25-30 pages
    BIZNESPLAN_MIN_SOURCES: int = 3  # Minimum sources per market claim
    BIZNESPLAN_MAX_ITERATIONS: int = 3  # Max refinement iterations
    BIZNESPLAN_QUALITY_THRESHOLD: float = 0.85  # Reviewer approval threshold
    
    # API Rate Limiting
    RATE_LIMIT_GENERATION: str = "10/minute"  # Max 10 generation requests per minute
    RATE_LIMIT_API: str = "100/minute"  # Max 100 API calls per minute
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "change-this-password"
    ALLOWED_HOSTS: list[str] = ["*"]  # Configure for production
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set Celery URLs to Redis if not specified
        if not self.CELERY_BROKER_URL:
            self.CELERY_BROKER_URL = self.REDIS_URL
        if not self.CELERY_RESULT_BACKEND:
            self.CELERY_RESULT_BACKEND = self.REDIS_URL


# Global settings instance
settings = Settings()
