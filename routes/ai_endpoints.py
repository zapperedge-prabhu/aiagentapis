import logging
from flask import Blueprint, request, jsonify
from middleware.auth import require_api_key, validate_request_data
from services.azure_storage import AzureBlobStorage
from services.file_processor import FileProcessor
from services.openai_service import OpenAIService
from utils.helpers import create_success_response, create_error_response, log_request_info, validate_file_path

logger = logging.getLogger(__name__)

# Create blueprint for AI endpoints
ai_bp = Blueprint('ai_endpoints', __name__)

# Initialize services
azure_storage = AzureBlobStorage()
file_processor = FileProcessor()
openai_service = OpenAIService()

@ai_bp.route('/summarize', methods=['POST'])
@require_api_key('/summarize')
@validate_request_data(['file_path'])
def summarize_document():
    """
    Summarize document content from Azure Blob Storage
    
    Expected JSON payload:
    {
        "file_path": "https://storagetest12344.blob.core.windows.net/container/filename.pdf"
    }
    """
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        
        log_request_info('summarize', file_path)
        
        if not validate_file_path(file_path):
            return create_error_response(
                "invalid_file_path", 
                "Invalid file path format", 
                400
            )
        
        # Download file from Azure Blob Storage
        file_content = azure_storage.download_blob_content(file_path)
        file_properties = azure_storage.get_blob_properties(file_path)
        
        # Extract text content
        text_content = file_processor.extract_text_from_content(
            file_content, 
            file_properties.get('content_type'), 
            file_properties.get('name')
        )
        
        # Validate text length
        text_content, was_truncated = file_processor.validate_text_length(text_content)
        
        # Generate summary
        result = openai_service.summarize_document(text_content)
        
        if not result.get('success'):
            return create_error_response(
                "summarization_failed", 
                result.get('error'), 
                500
            )
        
        response_data = {
            "file_path": file_path,
            "file_properties": file_properties,
            "summary": result.get('summary'),
            "original_length": result.get('original_length'),
            "summary_length": result.get('summary_length'),
            "was_truncated": was_truncated
        }
        
        return jsonify(create_success_response(response_data, "Document summarized successfully"))
        
    except FileNotFoundError as e:
        return create_error_response("file_not_found", str(e), 404)
    except ValueError as e:
        return create_error_response("processing_error", str(e), 400)
    except Exception as e:
        logger.error(f"Error in summarize endpoint: {e}")
        return create_error_response("internal_error", "An unexpected error occurred", 500)

@ai_bp.route('/sentiment', methods=['POST'])
@require_api_key('/sentiment')
@validate_request_data(['file_path'])
def analyze_sentiment():
    """
    Analyze sentiment of document content from Azure Blob Storage
    
    Expected JSON payload:
    {
        "file_path": "https://storagetest12344.blob.core.windows.net/container/filename.pdf"
    }
    """
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        
        log_request_info('sentiment', file_path)
        
        if not validate_file_path(file_path):
            return create_error_response(
                "invalid_file_path", 
                "Invalid file path format", 
                400
            )
        
        # Download and process file
        file_content = azure_storage.download_blob_content(file_path)
        file_properties = azure_storage.get_blob_properties(file_path)
        
        text_content = file_processor.extract_text_from_content(
            file_content, 
            file_properties.get('content_type'), 
            file_properties.get('name')
        )
        
        text_content, was_truncated = file_processor.validate_text_length(text_content)
        
        # Analyze sentiment
        result = openai_service.analyze_sentiment(text_content)
        
        if not result.get('success'):
            return create_error_response(
                "sentiment_analysis_failed", 
                result.get('error'), 
                500
            )
        
        response_data = {
            "file_path": file_path,
            "file_properties": file_properties,
            "sentiment": result.get('sentiment'),
            "confidence": result.get('confidence'),
            "explanation": result.get('explanation'),
            "was_truncated": was_truncated
        }
        
        return jsonify(create_success_response(response_data, "Sentiment analysis completed successfully"))
        
    except FileNotFoundError as e:
        return create_error_response("file_not_found", str(e), 404)
    except ValueError as e:
        return create_error_response("processing_error", str(e), 400)
    except Exception as e:
        logger.error(f"Error in sentiment endpoint: {e}")
        return create_error_response("internal_error", "An unexpected error occurred", 500)

@ai_bp.route('/extract-keywords', methods=['POST'])
@require_api_key('/extract-keywords')
@validate_request_data(['file_path'])
def extract_keywords():
    """
    Extract keywords from document content from Azure Blob Storage
    
    Expected JSON payload:
    {
        "file_path": "https://storagetest12344.blob.core.windows.net/container/filename.pdf"
    }
    """
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        
        log_request_info('extract-keywords', file_path)
        
        if not validate_file_path(file_path):
            return create_error_response(
                "invalid_file_path", 
                "Invalid file path format", 
                400
            )
        
        # Download and process file
        file_content = azure_storage.download_blob_content(file_path)
        file_properties = azure_storage.get_blob_properties(file_path)
        
        text_content = file_processor.extract_text_from_content(
            file_content, 
            file_properties.get('content_type'), 
            file_properties.get('name')
        )
        
        text_content, was_truncated = file_processor.validate_text_length(text_content)
        
        # Extract keywords
        result = openai_service.extract_keywords(text_content)
        
        if not result.get('success'):
            return create_error_response(
                "keyword_extraction_failed", 
                result.get('error'), 
                500
            )
        
        response_data = {
            "file_path": file_path,
            "file_properties": file_properties,
            "keywords": result.get('keywords'),
            "keyword_count": result.get('count'),
            "was_truncated": was_truncated
        }
        
        return jsonify(create_success_response(response_data, "Keywords extracted successfully"))
        
    except FileNotFoundError as e:
        return create_error_response("file_not_found", str(e), 404)
    except ValueError as e:
        return create_error_response("processing_error", str(e), 400)
    except Exception as e:
        logger.error(f"Error in extract-keywords endpoint: {e}")
        return create_error_response("internal_error", "An unexpected error occurred", 500)

@ai_bp.route('/translate', methods=['POST'])
@require_api_key('/translate')
@validate_request_data(['file_path', 'target_language'])
def translate_document():
    """
    Translate document content from Azure Blob Storage
    
    Expected JSON payload:
    {
        "file_path": "https://storagetest12344.blob.core.windows.net/container/filename.pdf",
        "target_language": "Hindi"
    }
    """
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        target_language = data.get('target_language')
        
        log_request_info('translate', file_path, {"target_language": target_language})
        
        if not validate_file_path(file_path):
            return create_error_response(
                "invalid_file_path", 
                "Invalid file path format", 
                400
            )
        
        # Download and process file
        file_content = azure_storage.download_blob_content(file_path)
        file_properties = azure_storage.get_blob_properties(file_path)
        
        text_content = file_processor.extract_text_from_content(
            file_content, 
            file_properties.get('content_type'), 
            file_properties.get('name')
        )
        
        text_content, was_truncated = file_processor.validate_text_length(text_content, 50000)  # Smaller limit for translation
        
        # Translate content
        result = openai_service.translate_text(text_content, target_language)
        
        if not result.get('success'):
            return create_error_response(
                "translation_failed", 
                result.get('error'), 
                500
            )
        
        response_data = {
            "file_path": file_path,
            "file_properties": file_properties,
            "translated_text": result.get('translated_text'),
            "source_language": result.get('source_language'),
            "target_language": result.get('target_language'),
            "original_length": result.get('original_length'),
            "translated_length": result.get('translated_length'),
            "was_truncated": was_truncated
        }
        
        return jsonify(create_success_response(response_data, "Document translated successfully"))
        
    except FileNotFoundError as e:
        return create_error_response("file_not_found", str(e), 404)
    except ValueError as e:
        return create_error_response("processing_error", str(e), 400)
    except Exception as e:
        logger.error(f"Error in translate endpoint: {e}")
        return create_error_response("internal_error", "An unexpected error occurred", 500)

@ai_bp.route('/structure-data', methods=['POST'])
@require_api_key('/structure-data')
@validate_request_data(['file_path'])
def structure_document_data():
    """
    Extract structured data from document content from Azure Blob Storage
    
    Expected JSON payload:
    {
        "file_path": "https://storagetest12344.blob.core.windows.net/container/filename.pdf"
    }
    """
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        
        log_request_info('structure-data', file_path)
        
        if not validate_file_path(file_path):
            return create_error_response(
                "invalid_file_path", 
                "Invalid file path format", 
                400
            )
        
        # Download and process file
        file_content = azure_storage.download_blob_content(file_path)
        file_properties = azure_storage.get_blob_properties(file_path)
        
        text_content = file_processor.extract_text_from_content(
            file_content, 
            file_properties.get('content_type'), 
            file_properties.get('name')
        )
        
        text_content, was_truncated = file_processor.validate_text_length(text_content)
        
        # Extract structured data
        result = openai_service.structure_data(text_content)
        
        if not result.get('success'):
            return create_error_response(
                "data_structuring_failed", 
                result.get('error'), 
                500
            )
        
        response_data = {
            "file_path": file_path,
            "file_properties": file_properties,
            "structured_data": result.get('structured_data'),
            "was_truncated": was_truncated
        }
        
        return jsonify(create_success_response(response_data, "Structured data extracted successfully"))
        
    except FileNotFoundError as e:
        return create_error_response("file_not_found", str(e), 404)
    except ValueError as e:
        return create_error_response("processing_error", str(e), 400)
    except Exception as e:
        logger.error(f"Error in structure-data endpoint: {e}")
        return create_error_response("internal_error", "An unexpected error occurred", 500)

@ai_bp.route('/detect-topics', methods=['POST'])
@require_api_key('/detect-topics')
@validate_request_data(['file_path'])
def detect_document_topics():
    """
    Detect topics in document content from Azure Blob Storage
    
    Expected JSON payload:
    {
        "file_path": "https://storagetest12344.blob.core.windows.net/container/filename.pdf"
    }
    """
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        
        log_request_info('detect-topics', file_path)
        
        if not validate_file_path(file_path):
            return create_error_response(
                "invalid_file_path", 
                "Invalid file path format", 
                400
            )
        
        # Download and process file
        file_content = azure_storage.download_blob_content(file_path)
        file_properties = azure_storage.get_blob_properties(file_path)
        
        text_content = file_processor.extract_text_from_content(
            file_content, 
            file_properties.get('content_type'), 
            file_properties.get('name')
        )
        
        text_content, was_truncated = file_processor.validate_text_length(text_content)
        
        # Detect topics
        result = openai_service.detect_topics(text_content)
        
        if not result.get('success'):
            return create_error_response(
                "topic_detection_failed", 
                result.get('error'), 
                500
            )
        
        response_data = {
            "file_path": file_path,
            "file_properties": file_properties,
            "topics": result.get('topics'),
            "topic_count": result.get('topic_count'),
            "was_truncated": was_truncated
        }
        
        return jsonify(create_success_response(response_data, "Topics detected successfully"))
        
    except FileNotFoundError as e:
        return create_error_response("file_not_found", str(e), 404)
    except ValueError as e:
        return create_error_response("processing_error", str(e), 400)
    except Exception as e:
        logger.error(f"Error in detect-topics endpoint: {e}")
        return create_error_response("internal_error", "An unexpected error occurred", 500)

# Health check endpoint
@ai_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "AI Agent API",
        "endpoints": [
            "/summarize",
            "/sentiment", 
            "/extract-keywords",
            "/translate",
            "/structure-data",
            "/detect-topics"
        ]
    })
