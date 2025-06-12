# Deployment Guide - AI Agent API Server

## Production Deployment Checklist

### Environment Setup
1. **Set Environment Variables:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export AZURE_STORAGE_CONNECTION_STRING="your-azure-connection-string"
   export SESSION_SECRET="production-secret-key"
   ```

2. **Configure API Keys for Production:**
   ```bash
   export SUMMARIZE_API_KEY="prod-summarize-key"
   export SENTIMENT_API_KEY="prod-sentiment-key"
   export KEYWORDS_API_KEY="prod-keywords-key"
   export TRANSLATE_API_KEY="prod-translate-key"
   export STRUCTURE_API_KEY="prod-structure-key"
   export TOPICS_API_KEY="prod-topics-key"
   ```

### Security Considerations
- Use strong, unique API keys for each endpoint
- Ensure Azure Storage has proper access controls
- Enable HTTPS in production
- Monitor API usage and rate limits
- Implement logging and monitoring

### Performance Optimization
- Consider connection pooling for Azure Storage
- Implement caching for frequently accessed files
- Monitor OpenAI API usage and costs
- Set appropriate timeout values
- Scale with multiple workers if needed

### Monitoring
- Monitor endpoint response times
- Track OpenAI API usage and costs
- Log all file processing activities
- Set up alerts for errors and failures

## API Documentation Summary

### Base URL
Production: `https://your-domain.com`
Development: `http://localhost:5000`

### Authentication
Each endpoint requires a specific API key in the `X-API-Key` header.

### Supported File Formats
- PDF documents
- Text files (TXT, MD, CSV, JSON, XML)

### Rate Limits
- Dependent on OpenAI API limits
- Recommended: Implement client-side rate limiting

### File Size Limits
- Text content limited to 100,000 characters (configurable)
- Translation limited to 50,000 characters for better performance

## Usage Examples

### Document Summarization
```bash
curl -X POST https://your-api.com/summarize \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-summarize-key" \
  -d '{"file_path": "documents/report.pdf"}'
```

### Sentiment Analysis
```bash
curl -X POST https://your-api.com/sentiment \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-sentiment-key" \
  -d '{"file_path": "feedback/customer-review.txt"}'
```

### Language Translation
```bash
curl -X POST https://your-api.com/translate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-translate-key" \
  -d '{"file_path": "docs/manual.pdf", "target_language": "Spanish"}'
```

## API Response Format

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
  "message": "Detailed error description"
}
```

## Cost Estimation

### OpenAI API Costs (estimated)
- Document Summarization: ~$0.01-0.05 per document
- Sentiment Analysis: ~$0.005-0.02 per document
- Keyword Extraction: ~$0.01-0.03 per document
- Translation: ~$0.02-0.10 per document
- Data Structuring: ~$0.02-0.08 per document
- Topic Detection: ~$0.01-0.05 per document

Costs depend on document length and complexity.

### Azure Storage Costs
- Minimal for document storage and retrieval
- Standard blob storage rates apply

## Production Recommendations

1. **Load Balancing:** Use multiple instances behind a load balancer
2. **Caching:** Implement Redis for frequently accessed results
3. **Database:** Add PostgreSQL for request logging and analytics
4. **Monitoring:** Use APM tools like New Relic or Datadog
5. **Backup:** Regular backups of configuration and logs
6. **SSL/TLS:** Use proper certificates for HTTPS
7. **CORS:** Configure CORS headers if serving web clients
8. **Rate Limiting:** Implement proper rate limiting per client

## Troubleshooting

### Common Issues
1. **401 Unauthorized:** Check API key configuration
2. **404 File Not Found:** Verify file path and Azure Storage access
3. **500 Internal Error:** Check OpenAI API key and quota
4. **Timeout:** Increase timeout for large documents

### Debug Mode
Set `DEBUG=true` in environment for detailed logging in development.

### Health Check
Use `GET /health` to verify service status and available endpoints.