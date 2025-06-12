import logging
from typing import Dict, Any
from flask import jsonify

logger = logging.getLogger(__name__)

def create_success_response(data: Dict[str, Any], message: str = None) -> Dict[str, Any]:
    """
    Create a standardized success response
    
    Args:
        data (Dict[str, Any]): Response data
        message (str): Optional success message
        
    Returns:
        Dict[str, Any]: Standardized response
    """
    response = {
        "status": "success",
        "data": data
    }
    
    if message:
        response["message"] = message
    
    return response

def create_error_response(error: str, message: str = None, status_code: int = 500) -> tuple:
    """
    Create a standardized error response
    
    Args:
        error (str): Error type/code
        message (str): Error message
        status_code (int): HTTP status code
        
    Returns:
        tuple: (response, status_code)
    """
    response = {
        "status": "error",
        "error": error
    }
    
    if message:
        response["message"] = message
    
    return jsonify(response), status_code

def log_request_info(endpoint: str, file_path: str = None, additional_info: Dict = None):
    """
    Log request information for monitoring
    
    Args:
        endpoint (str): API endpoint name
        file_path (str): File path being processed
        additional_info (Dict): Additional information to log
    """
    log_data = {
        "endpoint": endpoint,
        "file_path": file_path
    }
    
    if additional_info:
        log_data.update(additional_info)
    
    logger.info(f"Processing request: {log_data}")

def validate_file_path(file_path: str) -> bool:
    """
    Validate file path format
    
    Args:
        file_path (str): File path to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not file_path:
        return False
    
    # Check for basic path format
    if file_path.startswith('http'):
        # URL format validation
        return '/' in file_path and '.' in file_path.split('/')[-1]
    else:
        # Container/blob format validation
        return '/' in file_path and len(file_path.split('/')) >= 2
    
def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe processing
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    if not filename:
        return "unknown_file"
    
    # Remove path separators and dangerous characters
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_"
    sanitized = ''.join(c for c in filename if c in safe_chars)
    
    return sanitized if sanitized else "unknown_file"
