import logging
from functools import wraps
from flask import request, jsonify
from config import API_KEYS

logger = logging.getLogger(__name__)

def require_api_key(endpoint_path):
    """
    Decorator to require API key authentication for specific endpoints
    
    Args:
        endpoint_path (str): The endpoint path to validate against
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get API key from headers
            api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization')
            
            if api_key and api_key.startswith('Bearer '):
                api_key = api_key[7:]  # Remove 'Bearer ' prefix
            
            if not api_key:
                logger.warning(f"Missing API key for endpoint {endpoint_path}")
                return jsonify({
                    "error": "API key required",
                    "message": "Please provide API key in X-API-Key header or Authorization header"
                }), 401
            
            # Check if API key is valid for this endpoint
            expected_key = API_KEYS.get(endpoint_path)
            if not expected_key:
                logger.error(f"No API key configured for endpoint {endpoint_path}")
                return jsonify({
                    "error": "Endpoint not configured",
                    "message": "This endpoint is not properly configured"
                }), 500
            
            if api_key != expected_key:
                logger.warning(f"Invalid API key for endpoint {endpoint_path}")
                return jsonify({
                    "error": "Invalid API key",
                    "message": "The provided API key is not valid for this endpoint"
                }), 403
            
            logger.info(f"Valid API key provided for endpoint {endpoint_path}")
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def validate_request_data(required_fields=None):
    """
    Decorator to validate required fields in request data
    
    Args:
        required_fields (list): List of required field names
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if required_fields:
                data = request.get_json() if request.is_json else request.form
                
                if not data:
                    return jsonify({
                        "error": "Invalid request",
                        "message": "Request must contain JSON data or form data"
                    }), 400
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({
                        "error": "Missing required fields",
                        "message": f"The following fields are required: {', '.join(missing_fields)}"
                    }), 400
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
