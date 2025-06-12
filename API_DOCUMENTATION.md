# AI Agent API Server Documentation

## Overview

The AI Agent API Server is a Python Flask-based REST API that provides 6 distinct AI-powered endpoints for document processing using OpenAI's GPT-4o model. The server processes files from Azure Blob Storage and offers capabilities including document summarization, sentiment analysis, keyword extraction, translation, data structuring, and topic detection.

## Base URL

```
http://localhost:5000
```

## Authentication

Each endpoint requires a specific API key provided in the `X-API-Key` header:

| Endpoint | API Key |
|----------|---------|
| `/summarize` | `summarize-key-123` |
| `/sentiment` | `sentiment-key-123` |
| `/extract-keywords` | `keywords-key-123` |
| `/translate` | `translate-key-123` |
| `/structure-data` | `structure-key-123` |
| `/detect-topics` | `topics-key-123` |

## File Path Format

All endpoints require files to be specified using the full Azure Blob Storage URL format:

```
https://storagetest12344.blob.core.windows.net/container/filename.ext
```

## API Endpoints

### 1. Document Summarization

**Endpoint:** `POST /summarize`

**Description:** Generates a concise summary of document content.

**Headers:**
```
Content-Type: application/json
X-API-Key: summarize-key-123
```

**Request Body:**
```json
{
    "file_path": "https://storagetest12344.blob.core.windows.net/demo/sample-document.pdf"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Document summarized successfully",
    "data": {
        "file_path": "https://storagetest12344.blob.core.windows.net/demo/sample-document.pdf",
        "summary": "Detailed summary of the document content...",
        "summary_length": 250,
        "original_length": 1500,
        "was_truncated": false,
        "file_properties": {
            "name": "sample-document.pdf",
            "size": 45231,
            "content_type": "application/pdf",
            "last_modified": "2025-06-09T14:30:00Z"
        }
    }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/summarize \
  -H "Content-Type: application/json" \
  -H "X-API-Key: summarize-key-123" \
  -d '{"file_path": "https://storagetest12344.blob.core.windows.net/demo/sample-document.pdf"}'
```

### 2. Sentiment Analysis

**Endpoint:** `POST /sentiment`

**Description:** Analyzes the emotional tone and sentiment of document content.

**Headers:**
```
Content-Type: application/json
X-API-Key: sentiment-key-123
```

**Request Body:**
```json
{
    "file_path": "https://storagetest12344.blob.core.windows.net/demo/feedback.txt"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Sentiment analysis completed successfully",
    "data": {
        "file_path": "https://storagetest12344.blob.core.windows.net/demo/feedback.txt",
        "sentiment": "positive",
        "confidence": 0.95,
        "explanation": "The text expresses high satisfaction with clear positive indicators...",
        "was_truncated": false,
        "file_properties": {
            "name": "feedback.txt",
            "size": 751,
            "content_type": "text/plain",
            "last_modified": "2025-06-09T13:24:23Z"
        }
    }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/sentiment \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sentiment-key-123" \
  -d '{"file_path": "https://storagetest12344.blob.core.windows.net/demo/feedback.txt"}'
```

### 3. Keyword Extraction

**Endpoint:** `POST /extract-keywords`

**Description:** Identifies and extracts important keywords and phrases from document content.

**Headers:**
```
Content-Type: application/json
X-API-Key: keywords-key-123
```

**Request Body:**
```json
{
    "file_path": "https://storagetest12344.blob.core.windows.net/demo/research-paper.pdf"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Keywords extracted successfully",
    "data": {
        "file_path": "https://storagetest12344.blob.core.windows.net/demo/research-paper.pdf",
        "keywords": [
            "machine learning",
            "artificial intelligence",
            "data analysis",
            "neural networks",
            "deep learning"
        ],
        "keyword_count": 15,
        "was_truncated": false,
        "file_properties": {
            "name": "research-paper.pdf",
            "size": 234567,
            "content_type": "application/pdf",
            "last_modified": "2025-06-09T10:15:30Z"
        }
    }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/extract-keywords \
  -H "Content-Type: application/json" \
  -H "X-API-Key: keywords-key-123" \
  -d '{"file_path": "https://storagetest12344.blob.core.windows.net/demo/research-paper.pdf"}'
```

### 4. Document Translation

**Endpoint:** `POST /translate`

**Description:** Translates document content to a specified target language.

**Headers:**
```
Content-Type: application/json
X-API-Key: translate-key-123
```

**Request Body:**
```json
{
    "file_path": "https://storagetest12344.blob.core.windows.net/demo/english-doc.txt",
    "target_language": "Spanish"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Document translated successfully",
    "data": {
        "file_path": "https://storagetest12344.blob.core.windows.net/demo/english-doc.txt",
        "target_language": "Spanish",
        "original_text": "Hello, this is a sample document...",
        "translated_text": "Hola, este es un documento de muestra...",
        "was_truncated": false,
        "file_properties": {
            "name": "english-doc.txt",
            "size": 512,
            "content_type": "text/plain",
            "last_modified": "2025-06-09T09:45:12Z"
        }
    }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: translate-key-123" \
  -d '{"file_path": "https://storagetest12344.blob.core.windows.net/demo/english-doc.txt", "target_language": "Spanish"}'
```

### 5. Structured Data Extraction

**Endpoint:** `POST /structure-data`

**Description:** Extracts and organizes information into structured JSON format.

**Headers:**
```
Content-Type: application/json
X-API-Key: structure-key-123
```

**Request Body:**
```json
{
    "file_path": "https://storagetest12344.blob.core.windows.net/demo/invoice.pdf"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Structured data extracted successfully",
    "data": {
        "file_path": "https://storagetest12344.blob.core.windows.net/demo/invoice.pdf",
        "structured_data": {
            "document_type": "invoice",
            "invoice_number": "INV-2025-001",
            "date": "2025-06-09",
            "vendor": "ABC Company",
            "total_amount": 1250.00,
            "currency": "USD",
            "items": [
                {
                    "description": "Software License",
                    "quantity": 1,
                    "unit_price": 1250.00
                }
            ]
        },
        "was_truncated": false,
        "file_properties": {
            "name": "invoice.pdf",
            "size": 87654,
            "content_type": "application/pdf",
            "last_modified": "2025-06-09T11:20:45Z"
        }
    }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/structure-data \
  -H "Content-Type: application/json" \
  -H "X-API-Key: structure-key-123" \
  -d '{"file_path": "https://storagetest12344.blob.core.windows.net/demo/invoice.pdf"}'
```

### 6. Topic Detection

**Endpoint:** `POST /detect-topics`

**Description:** Identifies primary topics and themes within document content.

**Headers:**
```
Content-Type: application/json
X-API-Key: topics-key-123
```

**Request Body:**
```json
{
    "file_path": "https://storagetest12344.blob.core.windows.net/demo/article.txt"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Topics detected successfully",
    "data": {
        "file_path": "https://storagetest12344.blob.core.windows.net/demo/article.txt",
        "topics": [
            {
                "topic": "Technology",
                "confidence": 0.92,
                "keywords": ["AI", "machine learning", "automation"]
            },
            {
                "topic": "Business Strategy",
                "confidence": 0.78,
                "keywords": ["growth", "market", "innovation"]
            }
        ],
        "primary_topic": "Technology",
        "topic_count": 2,
        "was_truncated": false,
        "file_properties": {
            "name": "article.txt",
            "size": 3456,
            "content_type": "text/plain",
            "last_modified": "2025-06-09T16:30:22Z"
        }
    }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/detect-topics \
  -H "Content-Type: application/json" \
  -H "X-API-Key: topics-key-123" \
  -d '{"file_path": "https://storagetest12344.blob.core.windows.net/demo/article.txt"}'
```

### 7. Health Check

**Endpoint:** `GET /health`

**Description:** Returns the health status of the API server.

**Headers:**
```
Content-Type: application/json
```

**Response:**
```json
{
    "status": "healthy",
    "message": "AI Agent API Server is running",
    "timestamp": "2025-06-09T16:45:30Z",
    "version": "1.0.0"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/health
```

## Error Responses

### Authentication Error
```json
{
    "status": "error",
    "error": "authentication_error",
    "message": "Invalid or missing API key for this endpoint"
}
```

### Invalid File Path
```json
{
    "status": "error",
    "error": "processing_error",
    "message": "Invalid file path. Only full Azure Blob Storage URLs are supported. Format: https://storagetest12344.blob.core.windows.net/container/filename.ext"
}
```

### File Not Found
```json
{
    "status": "error",
    "error": "file_not_found",
    "message": "The specified file could not be found in Azure Blob Storage"
}
```

### Processing Error
```json
{
    "status": "error",
    "error": "processing_error",
    "message": "Error processing document: [specific error details]"
}
```

### OpenAI API Error
```json
{
    "status": "error",
    "error": "ai_processing_error",
    "message": "Error communicating with OpenAI API: [specific error details]"
}
```

## Supported File Types

- **PDF Documents** (.pdf)
- **Text Files** (.txt, .md)
- **Microsoft Word** (.docx)
- **Rich Text Format** (.rtf)

## Rate Limits

- **Requests per minute:** 60
- **Maximum file size:** 10MB
- **Text length limit:** 100,000 characters (automatically truncated if exceeded)

## Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (missing required fields) |
| 401 | Unauthorized (invalid API key) |
| 404 | File Not Found |
| 405 | Method Not Allowed |
| 500 | Internal Server Error |

## Python SDK Example

```python
import requests

class AIAgentClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.api_keys = {
            'summarize': 'summarize-key-123',
            'sentiment': 'sentiment-key-123',
            'keywords': 'keywords-key-123',
            'translate': 'translate-key-123',
            'structure': 'structure-key-123',
            'topics': 'topics-key-123'
        }
    
    def summarize_document(self, file_path):
        """Summarize a document from Azure Blob Storage"""
        return self._make_request('/summarize', {
            'file_path': file_path
        }, self.api_keys['summarize'])
    
    def analyze_sentiment(self, file_path):
        """Analyze sentiment of a document"""
        return self._make_request('/sentiment', {
            'file_path': file_path
        }, self.api_keys['sentiment'])
    
    def extract_keywords(self, file_path):
        """Extract keywords from a document"""
        return self._make_request('/extract-keywords', {
            'file_path': file_path
        }, self.api_keys['keywords'])
    
    def translate_document(self, file_path, target_language):
        """Translate a document to target language"""
        return self._make_request('/translate', {
            'file_path': file_path,
            'target_language': target_language
        }, self.api_keys['translate'])
    
    def structure_data(self, file_path):
        """Extract structured data from a document"""
        return self._make_request('/structure-data', {
            'file_path': file_path
        }, self.api_keys['structure'])
    
    def detect_topics(self, file_path):
        """Detect topics in a document"""
        return self._make_request('/detect-topics', {
            'file_path': file_path
        }, self.api_keys['topics'])
    
    def _make_request(self, endpoint, data, api_key):
        """Make HTTP request to API"""
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        }
        response = requests.post(
            f"{self.base_url}{endpoint}", 
            json=data, 
            headers=headers
        )
        return response.json()

# Usage example
client = AIAgentClient()
result = client.summarize_document(
    "https://storagetest12344.blob.core.windows.net/demo/sample.pdf"
)
print(result)
```

## JavaScript SDK Example

```javascript
class AIAgentClient {
    constructor(baseUrl = 'http://localhost:5000') {
        this.baseUrl = baseUrl;
        this.apiKeys = {
            summarize: 'summarize-key-123',
            sentiment: 'sentiment-key-123',
            keywords: 'keywords-key-123',
            translate: 'translate-key-123',
            structure: 'structure-key-123',
            topics: 'topics-key-123'
        };
    }

    async summarizeDocument(filePath) {
        return this._makeRequest('/summarize', {
            file_path: filePath
        }, this.apiKeys.summarize);
    }

    async analyzeSentiment(filePath) {
        return this._makeRequest('/sentiment', {
            file_path: filePath
        }, this.apiKeys.sentiment);
    }

    async extractKeywords(filePath) {
        return this._makeRequest('/extract-keywords', {
            file_path: filePath
        }, this.apiKeys.keywords);
    }

    async translateDocument(filePath, targetLanguage) {
        return this._makeRequest('/translate', {
            file_path: filePath,
            target_language: targetLanguage
        }, this.apiKeys.translate);
    }

    async structureData(filePath) {
        return this._makeRequest('/structure-data', {
            file_path: filePath
        }, this.apiKeys.structure);
    }

    async detectTopics(filePath) {
        return this._makeRequest('/detect-topics', {
            file_path: filePath
        }, this.apiKeys.topics);
    }

    async _makeRequest(endpoint, data, apiKey) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': apiKey
            },
            body: JSON.stringify(data)
        });
        return response.json();
    }
}

// Usage example
const client = new AIAgentClient();
client.summarizeDocument('https://storagetest12344.blob.core.windows.net/demo/sample.pdf')
    .then(result => console.log(result));
```

## Environment Variables

The server requires the following environment variables:

```bash
OPENAI_API_KEY=your_openai_api_key_here
AZURE_STORAGE_CONNECTION_STRING=your_azure_connection_string_here
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY pip-requirements.txt .
RUN pip install -r pip-requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--reuse-port", "--reload", "main:app"]
```

### Production Configuration

For production deployment:

1. Set environment variables for OpenAI and Azure credentials
2. Configure proper API key management
3. Set up SSL/TLS termination
4. Configure rate limiting and monitoring
5. Use a production WSGI server (included: Gunicorn)

---

**Last Updated:** June 9, 2025  
**API Version:** 1.0.0  
**Server Status:** Production Ready