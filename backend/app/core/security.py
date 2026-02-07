"""
Security utilities for the application.
Includes CORS configuration, input validation, and rate limiting helpers.
"""

from typing import List
import re
from app.core.config import settings


def get_cors_config() -> dict:
    """
    Get CORS configuration for FastAPI.
    
    Returns:
        Dictionary with CORS settings
    """
    return {
        "allow_origins": ["*"],  # Allow all origins including file://
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }


def sanitize_input(text: str, max_length: int = 10000) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
        
    Raises:
        ValueError: If input is too long
    """
    if len(text) > max_length:
        raise ValueError(f"Input too long. Maximum {max_length} characters allowed.")
    
    # Remove potentially harmful characters
    # Keep alphanumeric, spaces, and common punctuation
    sanitized = re.sub(r'[^\w\s\-.,!?:;()\[\]{}"\'/]', '', text)
    
    return sanitized.strip()


def validate_conversation_id(conversation_id: str) -> bool:
    """
    Validate conversation ID format.
    
    Args:
        conversation_id: Conversation ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    # UUID format check (simple version)
    pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
    return bool(re.match(pattern, conversation_id.lower()))


def validate_file_extension(filename: str) -> bool:
    """
    Validate file extension against supported types.
    
    Args:
        filename: File name to validate
        
    Returns:
        True if valid, False otherwise
    """
    extension = filename.lower().split('.')[-1]
    return extension in settings.supported_file_types_list


def get_rate_limit_key(endpoint: str) -> str:
    """
    Get rate limit configuration for an endpoint.
    
    Args:
        endpoint: Endpoint name (e.g., 'chat', 'upload')
        
    Returns:
        Rate limit string (e.g., '10/minute')
    """
    rate_limits = {
        "chat": settings.RATE_LIMIT_CHAT,
        "upload": settings.RATE_LIMIT_UPLOAD,
    }
    return rate_limits.get(endpoint, "20/minute")  # Default limit


