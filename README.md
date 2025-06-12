# AI Agent API Server

A Python Flask REST API server that demonstrates OpenAI capabilities through AI agent endpoints that process files from Azure Blob Storage.

## Features

- **Document Summarization** - Generate concise summaries of documents
- **Sentiment Analysis** - Analyze emotional tone and sentiment
- **Keyword Extraction** - Extract important keywords and phrases
- **Language Translation** - Translate documents to different languages
- **Structured Data Extraction** - Extract entities, dates, amounts, and contact info
- **Topic Detection** - Identify primary topics and themes

## Supported File Formats

- PDF files (.pdf)
- Text files (.txt, .md, .csv, .json, .xml)

## API Endpoints

### Health Check
```
GET /health
```
Returns service status and available endpoints.

### Document Summarization
```
POST /summarize
```
**Headers:**
- `X-API-Key: summarize-key-123`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "file_path": "container/filename.pdf"
}
```

### Sentiment Analysis
```
POST /sentiment
```
**Headers:**
- `X-API-Key: sentiment-key-123`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "file_path": "container/filename.pdf"
}
```

### Keyword Extraction
```
POST /extract-keywords
```
**Headers:**
- `X-API-Key: keywords-key-123`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "file_path": "container/filename.pdf"
}
```

### Language Translation
```
POST /translate
```
**Headers:**
- `X-API-Key: translate-key-123`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "file_path": "container/filename.pdf",
  "target_language": "Hindi"
}
```

### Structured Data Extraction
```
POST /structure-data
```
**Headers:**
- `X-API-Key: structure-key-123`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "file_path": "container/filename.pdf"
}
```

### Topic Detection
```
POST /detect-topics
```
**Headers:**
- `X-API-Key: topics-key-123`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "file_path": "container/filename.pdf"
}
```

## File Path Format

Files must be specified using the full Azure Blob Storage URL format:

**Full URL format:** `https://storagetest12344.blob.core.windows.net/container/blob-name.ext`

This ensures clarity and prevents confusion in API usage.

## Authentication

Each endpoint requires a specific API key provided in the `X-API-Key` header:

- `/summarize` → `summarize-key-123`
- `/sentiment` → `sentiment-key-123`
- `/extract-keywords` → `keywords-key-123`
- `/translate` → `translate-key-123`
- `/structure-data` → `structure-key-123`
- `/detect-topics` → `topics-key-123`

## Response Format

### Success Response
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": {
    "file_path": "container/filename.pdf",
    "file_properties": {
      "content_type": "application/pdf",
      "size": 12345,
      "last_modified": "2025-06-09T13:20:00Z",
      "name": "filename.pdf"
    },
    "result": "..."
  }
}
```

### Error Response
```json
{
  "status": "error",
  "error": "error_code",
  "message": "Error description"
}
```

## Configuration

The application is configured through environment variables:

- `OPENAI_API_KEY` - OpenAI API key for AI processing
- `AZURE_STORAGE_CONNECTION_STRING` - Azure Blob Storage connection string
- Individual endpoint API keys (SUMMARIZE_API_KEY, SENTIMENT_API_KEY, etc.)

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-openai-key"
export AZURE_STORAGE_CONNECTION_STRING="your-azure-connection-string"

# Run the application
python main.py
```

The server will start on `http://0.0.0.0:5000` by default.

## Example Usage

```bash
# Test health endpoint
curl -X GET http://localhost:5000/health

# Summarize a document
curl -X POST http://localhost:5000/summarize \
  -H "Content-Type: application/json" \
  -H "X-API-Key: summarize-key-123" \
  -d '{"file_path": "documents/report.pdf"}'

# Analyze sentiment
curl -X POST http://localhost:5000/sentiment \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sentiment-key-123" \
  -d '{"file_path": "documents/feedback.txt"}'

# Translate document
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: translate-key-123" \
  -d '{"file_path": "documents/article.pdf", "target_language": "Spanish"}'
```

## Architecture

- **Flask** - Web framework
- **OpenAI GPT-4o** - AI processing engine
- **Azure Blob Storage** - Document storage
- **PyPDF2** - PDF text extraction
- **Gunicorn** - WSGI server

## Error Handling

The API includes comprehensive error handling for:
- Invalid API keys
- Missing files in Azure storage
- Unsupported file formats
- Network connectivity issues
- OpenAI API errors
- Text processing limitations