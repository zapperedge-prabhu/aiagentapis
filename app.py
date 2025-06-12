import os
import logging
from flask import Flask, jsonify
from routes.ai_endpoints import ai_bp
from config import SECRET_KEY, DEBUG

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configure app
    app.secret_key = SECRET_KEY
    app.config['DEBUG'] = DEBUG
    
    # Register blueprints
    app.register_blueprint(ai_bp)
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            "service": "AI Agent API Server",
            "description": "Python Flask REST API demonstrating OpenAI capabilities with Azure Blob Storage",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "summarize": "/summarize",
                "sentiment": "/sentiment",
                "extract_keywords": "/extract-keywords",
                "translate": "/translate",
                "structure_data": "/structure-data",
                "detect_topics": "/detect-topics"
            },
            "authentication": "Each endpoint requires X-API-Key header with endpoint-specific API key",
            "documentation": {
                "file_path_format": "container/filename.ext or full blob URL",
                "supported_formats": ["PDF", "TXT", "MD", "CSV", "JSON", "XML"],
                "required_headers": ["X-API-Key", "Content-Type: application/json"]
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "error": "not_found",
            "message": "The requested endpoint was not found"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "status": "error",
            "error": "method_not_allowed",
            "message": "The request method is not allowed for this endpoint"
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            "status": "error",
            "error": "internal_server_error",
            "message": "An internal server error occurred"
        }), 500
    
    logger.info("Flask application created and configured successfully")
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    from config import HOST, PORT
    logger.info(f"Starting AI Agent API Server on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=DEBUG)
