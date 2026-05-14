"""
Configuration and enums for Omni Executor.
"""

from enum import Enum


class ServiceTier(Enum):
    """Service tier options."""
    STARTER = "Starter"
    PRO = "Pro"
    ENTERPRISE = "Enterprise"
    CUSTOM = "Custom Consulting"


class BusinessScale(Enum):
    """Business scale options."""
    SMALL_BUSINESS = "Small Business"
    MEDIUM_BUSINESS = "Medium Business"
    LARGE_COMPANY = "Large Company"
    ENTERPRISE = "Enterprise"
    AGENCY = "Agency"
    NGO = "NGO"
    GOVERNMENT = "Government Office"
    INSTITUTION = "Institution"


class BusinessCategory(Enum):
    """Business category options."""
    OPERATIONS = "Operations"
    FINANCE = "Finance"
    STRATEGY = "Strategy"
    ORGANIZATION = "Organization & HR"
    CUSTOMER = "Customer & Sales"
    COMPLIANCE = "Compliance & Risk"
    TECHNOLOGY = "Technology & Systems"
    GROWTH = "Growth & Scaling"


class LLMProvider(Enum):
    """LLM provider options."""
    GEMINI = "gemini"
    OPENROUTER = "openrouter"
    CLAUDE = "claude"
    OPENAI = "openai"
    RULE_BASED = "rule_based"


class AppConfig:
    """Application configuration."""
    
    # Application info
    APP_NAME = "Omni Executor"
    VERSION = "1.0.0"
    DESCRIPTION = "Enterprise Reasoning Engine for Business Execution"
    
    # Analysis settings
    MAX_FILE_SIZE_MB = 50
    SUPPORTED_FILE_TYPES = ["csv", "xlsx"]
    
    # Default analysis parameters
    DEFAULT_ANALYSIS_DEPTH = 3
    DEFAULT_CONFIDENCE_THRESHOLD = 0.8
    
    # API providers
    SUPPORTED_LLM_PROVIDERS = ["gemini", "openrouter", "claude", "openai"]
    
    # Qdrant vector DB
    QDRANT_ENABLED = True
    QDRANT_HOST = "localhost"
    QDRANT_PORT = 6333
    
    # Service tier features
    TIER_FEATURES = {
        "Starter": {
            "max_analyses_per_month": 10,
            "max_file_size_mb": 10,
            "analysis_depth": 2,
            "email_export": False,
            "api_access": False,
            "vector_search": False,
        },
        "Pro": {
            "max_analyses_per_month": 100,
            "max_file_size_mb": 50,
            "analysis_depth": 4,
            "email_export": True,
            "api_access": True,
            "vector_search": True,
        },
        "Enterprise": {
            "max_analyses_per_month": 10000,
            "max_file_size_mb": 500,
            "analysis_depth": 5,
            "email_export": True,
            "api_access": True,
            "vector_search": True,
            "multi_agent": True,
            "custom_workflows": True,
        },
        "Custom Consulting": {
            "max_analyses_per_month": "unlimited",
            "max_file_size_mb": "unlimited",
            "analysis_depth": 5,
            "email_export": True,
            "api_access": True,
            "vector_search": True,
            "multi_agent": True,
            "custom_workflows": True,
            "dedicated_support": True,
        },
    }
    
    # Model configurations
    GEMINI_MODEL = "gemini-1.5-pro"
    OPENROUTER_MODEL = "anthropic/claude-3-sonnet"
    CLAUDE_MODEL = "claude-3-sonnet-20240229"
    OPENAI_MODEL = "gpt-4-turbo-preview"
    
    # Embedding model for Qdrant
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION = 384
