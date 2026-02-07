"""
Core configuration management using Pydantic Settings.
Loads configuration from environment variables with validation.
"""

from functools import lru_cache
from typing import List, Optional
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, validator
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # =============================================================================
    # API Configuration
    # =============================================================================
    API_HOST: str = Field(default="0.0.0.0", description="API host")
    API_PORT: int = Field(default=8000, description="API port")
    API_ENV: str = Field(default="development", description="Environment: development, production")
    API_RELOAD: bool = Field(default=True, description="Auto-reload on code changes")
    
    # =============================================================================
    # Company Settings
    # =============================================================================
    COMPANY_NAME: str = Field(default="MHK Tech Inc", description="Company name for chatbot context")
    
    # =============================================================================
    # LLM Configuration
    # =============================================================================

    

    # Company settings
    COMPANY_NAME: str = Field(default="MHKTech", description="Company name for prompts")
    MAX_CONVERSATION_HISTORY: int = Field(default=10, description="Max conversation messages to keep")
    LLM_PROVIDER: str = "openai"
    # OpenAI settings
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key from .env file")
    OPENAI_MODEL: str = Field(default="gpt-4o", description="OpenAI model name")
    OPENAI_TEMPERATURE: float = Field(default=0.7, description="OpenAI temperature")
    OPENAI_MAX_TOKENS: int = Field(default=500, description="Max tokens for OpenAI response")
    
    # =============================================================================
    # Embeddings Configuration
    # =============================================================================
    EMBEDDING_PROVIDER: str = Field(default="sentence-transformers", description="Embedding provider")
    OPENAI_EMBEDDING_MODEL: str = Field(default="text-embedding-3-small", description="OpenAI embedding model")
    
    # =============================================================================
    # Qdrant Vector Database
    # =============================================================================
    QDRANT_HOST: str = Field(default="localhost", description="Qdrant host")
    QDRANT_PORT: int = Field(default=6333, description="Qdrant port")
    QDRANT_COLLECTION_NAME: str = Field(default="company_docs", description="Qdrant collection name")
    QDRANT_VECTOR_SIZE: int = Field(default=1536, description="Vector dimension size (1536 for text-embedding-3-small)")
    
    # =============================================================================
    # Document Processing
    # =============================================================================
    CHUNK_SIZE: int = Field(default=1000, description="Text chunk size in characters")
    CHUNK_OVERLAP: int = Field(default=200, description="Overlap between chunks")
    CHUNKING_SEPARATORS: List[str] = Field(
        default=["\n\n", "\n", ". ", "! ", "? ", ", ", " ", ""],
        description="Separators for recursive chunking"
    )

    # Semantic Chunking Configuration
    SEMANTIC_SIMILARITY_THRESHOLD: float = Field(default=0.75, description="Threshold for semantic similarity")
    SEMANTIC_MIN_CHUNK_SIZE: int = Field(default=100, description="Minimum chunk size for semantic chunking")
    SEMANTIC_MAX_CHUNK_SIZE: int = Field(default=2000, description="Maximum chunk size for semantic chunking")

    SUPPORTED_FILE_TYPES: str = Field(default="pdf,docx,md,txt", description="Comma-separated supported file types")
    MAX_FILE_SIZE_MB: int = Field(default=50, description="Maximum file size in MB")

    # Document paths (relative to project root)
    RAW_DOCUMENTS_PATH: str = Field(default="data/documents/raw", description="Path to raw documents")
    PROCESSED_DOCUMENTS_PATH: str = Field(default="data/documents/processed", description="Path to processed documents")

    @property
    def project_root(self) -> Path:
        """Get the project root directory."""
        # Go up from backend/app/core to project root
        return Path(__file__).parent.parent.parent.parent

    @property
    def raw_documents_path_absolute(self) -> str:
        """Get absolute path to raw documents."""
        return str(self.project_root / self.RAW_DOCUMENTS_PATH)

    @property
    def processed_documents_path_absolute(self) -> str:
        """Get absolute path to processed documents."""
        return str(self.project_root / self.PROCESSED_DOCUMENTS_PATH)
    
    # =============================================================================
    # Retrieval Configuration
    # =============================================================================
    RETRIEVAL_TOP_K: int = Field(default=5, description="Number of documents to retrieve")
    RETRIEVAL_FETCH_K: int = Field(default=20, description="Number of candidates for MMR")
    RETRIEVAL_LAMBDA_MULT: float = Field(default=0.7, description="MMR lambda (relevance vs diversity)")
    
    # =============================================================================
    # Memory Configuration
    # =============================================================================
    CONVERSATION_MEMORY_TYPE: str = Field(default="buffer_window", description="Memory type")
    CONVERSATION_MEMORY_K: int = Field(default=10, description="Number of messages to remember")
    
    # =============================================================================
    # Security
    # =============================================================================
    SECRET_KEY: str = Field(default="change-me-in-production", description="Secret key for security")
    CORS_ORIGINS: str = Field(default="http://localhost:3000,http://localhost:8000", description="CORS origins")
    ALLOWED_HOSTS: str = Field(default="*", description="Allowed hosts")
    
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    RATE_LIMIT_CHAT: str = Field(default="10/minute", description="Chat endpoint rate limit")
    RATE_LIMIT_UPLOAD: str = Field(default="5/minute", description="Upload endpoint rate limit")
    
    # =============================================================================
    # Logging
    # =============================================================================
    LOG_LEVEL: str = Field(default="INFO", description="Log level")
    LOG_FILE: str = Field(default="data/logs/backend/app.log", description="Log file path")
    LOG_ROTATION: str = Field(default="10 MB", description="Log rotation size")
    LOG_RETENTION: str = Field(default="30 days", description="Log retention period")
    
    # =============================================================================
    # Performance
    # =============================================================================
    ENABLE_METRICS: bool = Field(default=False, description="Enable Prometheus metrics")
    PROMETHEUS_PORT: int = Field(default=9090, description="Prometheus port")
    ENABLE_EMBEDDING_CACHE: bool = Field(default=True, description="Enable embedding cache")
    CACHE_MAX_SIZE: int = Field(default=1000, description="Max cache entries")
    
    # =============================================================================
    # Validators
    # =============================================================================
    
    @validator("API_ENV")
    def validate_env(cls, v):
        """Validate environment value."""
        if v not in ["development", "production", "staging"]:
            raise ValueError("API_ENV must be development, production, or staging")
        return v
    
    
    # @validator("LLM_PROVIDER")
    # def validate_llm_provider(cls, v):
    #     """Validate LLM provider."""
    #     if v not in ["ollama", "openai"]:
    #         raise ValueError("LLM_PROVIDER must be ollama or openai")
    #     return v
    
    
    @validator("EMBEDDING_PROVIDER")
    def validate_embedding_provider(cls, v):
        """Validate embedding provider."""
        if v not in ["sentence-transformers", "openai"]:
            raise ValueError("EMBEDDING_PROVIDER must be sentence-transformers or openai")
        return v
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """Validate log level."""
        if v not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("LOG_LEVEL must be DEBUG, INFO, WARNING, ERROR, or CRITICAL")
        return v
    
    # =============================================================================
    # Helper Properties
    # =============================================================================
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.API_ENV == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.API_ENV == "production"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def supported_file_types_list(self) -> List[str]:
        """Get supported file types as list."""
        return [ft.strip() for ft in self.SUPPORTED_FILE_TYPES.split(",")]
    
    @property
    def max_file_size_bytes(self) -> int:
        """Get max file size in bytes."""
        return self.MAX_FILE_SIZE_MB * 1024 * 1024
    
    @property
    def qdrant_url(self) -> str:
        """Get Qdrant connection URL."""
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to ensure settings are loaded only once.
    """
    return Settings()


# Global settings instance
settings = get_settings()
