from app import app
from config import HOST, PORT, DEBUG
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info(f"Starting AI Agent API Server on {HOST}:{PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info("Available endpoints:")
    logger.info("  GET  / - API documentation")
    logger.info("  GET  /health - Health check")
    logger.info("  POST /summarize - Document summarization")
    logger.info("  POST /sentiment - Sentiment analysis")
    logger.info("  POST /extract-keywords - Keyword extraction")
    logger.info("  POST /translate - Language translation")
    logger.info("  POST /structure-data - Structured data extraction")
    logger.info("  POST /detect-topics - Topic detection")
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
