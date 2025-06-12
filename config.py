import os

# Azure Blob Storage Configuration
AZURE_STORAGE_CONNECTION_STRING = os.environ.get(
    "AZURE_STORAGE_CONNECTION_STRING",
    "DefaultEndpointsProtocol=https;AccountName=storagetest12344;AccountKey=lqsllsU65jg1xYs8Wlu3CIvIrwPu8vAbnuWR6cZrm3pH0Qt7aFJid+NYR7CGvGfzitYLOPP7yxwm+AStxmNhwA==;EndpointSuffix=core.windows.net"
)

# OpenAI Configuration
OPENAI_API_KEY = os.environ.get(
    "OPENAI_API_KEY",
    "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"
)

# API Keys for individual endpoints
API_KEYS = {
    "/summarize": os.environ.get("SUMMARIZE_API_KEY", "summarize-key-123"),
    "/sentiment": os.environ.get("SENTIMENT_API_KEY", "sentiment-key-123"),
    "/extract-keywords": os.environ.get("KEYWORDS_API_KEY", "keywords-key-123"),
    "/translate": os.environ.get("TRANSLATE_API_KEY", "translate-key-123"),
    "/structure-data": os.environ.get("STRUCTURE_API_KEY", "structure-key-123"),
    "/detect-topics": os.environ.get("TOPICS_API_KEY", "topics-key-123"),
}

# Flask Configuration
SECRET_KEY = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
PORT = int(os.environ.get("PORT", 8000))
HOST = "0.0.0.0"
