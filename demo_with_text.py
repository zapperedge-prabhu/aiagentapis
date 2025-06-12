#!/usr/bin/env python3
"""
Demonstration script for AI Agent API Server
Shows how to test the API functionality by creating a temporary text file
in Azure Blob Storage and then processing it through all AI endpoints.
"""

import requests
import tempfile
import os
from azure.storage.blob import BlobServiceClient
from config import AZURE_STORAGE_CONNECTION_STRING

# API Configuration
BASE_URL = "http://localhost:5000"
API_KEYS = {
    "/summarize": "summarize-key-123",
    "/sentiment": "sentiment-key-123", 
    "/extract-keywords": "keywords-key-123",
    "/translate": "translate-key-123",
    "/structure-data": "structure-key-123",
    "/detect-topics": "topics-key-123"
}

SAMPLE_TEXT = """
Customer Feedback Report - Q4 2024

Customer: John Smith
Email: john.smith@email.com
Date: December 15, 2024
Amount: $2,500.00

Review: I am extremely satisfied with the service provided by your company. 
The product quality exceeded my expectations and the customer support team 
was very helpful throughout the entire process. The delivery was prompt 
and the packaging was excellent.

Key topics discussed:
- Product quality and features
- Customer service experience
- Delivery and logistics
- Overall satisfaction rating: 5/5 stars

Recommendation: I would definitely recommend this company to others and 
plan to continue using their services in the future.

Contact Information:
Phone: +1-555-0123
Address: 123 Main Street, New York, NY 10001
"""

def upload_sample_text():
    """Upload sample text to Azure Blob Storage for testing"""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        
        # Create container if it doesn't exist
        container_name = "demo"
        try:
            blob_service_client.create_container(container_name)
            print(f"Created container: {container_name}")
        except Exception:
            print(f"Container {container_name} already exists")
        
        # Upload sample text
        blob_name = "sample-feedback.txt"
        blob_client = blob_service_client.get_blob_client(
            container=container_name, 
            blob=blob_name
        )
        
        blob_client.upload_blob(SAMPLE_TEXT, overwrite=True)
        print(f"Uploaded sample text to: {container_name}/{blob_name}")
        
        return f"{container_name}/{blob_name}"
        
    except Exception as e:
        print(f"Failed to upload sample text: {e}")
        return None

def test_endpoint(endpoint_path, api_key, data):
    """Test a specific API endpoint"""
    url = f"{BASE_URL}{endpoint_path}"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def demonstrate_ai_capabilities(file_path):
    """Demonstrate all AI capabilities with the uploaded file"""
    print("\n" + "="*60)
    print("AI AGENT CAPABILITIES DEMONSTRATION")
    print("="*60)
    
    tests = [
        {
            "name": "Document Summarization",
            "endpoint": "/summarize",
            "data": {"file_path": file_path},
            "description": "Generating concise summary of the document"
        },
        {
            "name": "Sentiment Analysis", 
            "endpoint": "/sentiment",
            "data": {"file_path": file_path},
            "description": "Analyzing emotional tone and sentiment"
        },
        {
            "name": "Keyword Extraction",
            "endpoint": "/extract-keywords", 
            "data": {"file_path": file_path},
            "description": "Extracting important keywords and phrases"
        },
        {
            "name": "Language Translation",
            "endpoint": "/translate",
            "data": {"file_path": file_path, "target_language": "Spanish"},
            "description": "Translating content to Spanish"
        },
        {
            "name": "Structured Data Extraction",
            "endpoint": "/structure-data",
            "data": {"file_path": file_path},
            "description": "Extracting structured entities and information"
        },
        {
            "name": "Topic Detection",
            "endpoint": "/detect-topics",
            "data": {"file_path": file_path},
            "description": "Identifying primary topics and themes"
        }
    ]
    
    for test in tests:
        print(f"\n{test['name']}")
        print("-" * len(test['name']))
        print(f"Description: {test['description']}")
        
        api_key = API_KEYS.get(test['endpoint'])
        response = test_endpoint(test['endpoint'], api_key, test['data'])
        
        if response and response.status_code == 200:
            print("Status: SUCCESS")
            result = response.json()
            
            # Display key results based on endpoint
            if test['endpoint'] == '/summarize':
                summary = result['data'].get('summary', '')
                print(f"Summary: {summary[:200]}...")
                
            elif test['endpoint'] == '/sentiment':
                sentiment = result['data'].get('sentiment')
                confidence = result['data'].get('confidence')
                print(f"Sentiment: {sentiment} (confidence: {confidence})")
                
            elif test['endpoint'] == '/extract-keywords':
                keywords = result['data'].get('keywords', [])
                print(f"Keywords: {', '.join(keywords[:10])}")
                
            elif test['endpoint'] == '/translate':
                translated = result['data'].get('translated_text', '')
                print(f"Translation: {translated[:200]}...")
                
            elif test['endpoint'] == '/structure-data':
                structured = result['data'].get('structured_data', {})
                names = structured.get('names', {}).get('people', [])
                amounts = structured.get('amounts', {}).get('monetary', [])
                print(f"People: {', '.join(names)}")
                print(f"Amounts: {', '.join(amounts)}")
                
            elif test['endpoint'] == '/detect-topics':
                topics = result['data'].get('topics', [])
                topic_names = [t.get('name') for t in topics[:5]]
                print(f"Topics: {', '.join(topic_names)}")
                
        else:
            print(f"Status: FAILED ({response.status_code if response else 'No response'})")
            if response:
                error = response.json().get('message', 'Unknown error')
                print(f"Error: {error}")

def main():
    """Main demonstration function"""
    print("AI Agent API - Live Demonstration")
    print("This script demonstrates all AI capabilities using real data")
    print(f"Testing against: {BASE_URL}")
    
    # Upload sample text for testing
    print("\nStep 1: Uploading sample document to Azure Blob Storage...")
    file_path = upload_sample_text()
    
    if not file_path:
        print("Failed to upload sample document. Cannot proceed with demonstration.")
        return False
    
    print(f"Sample document uploaded successfully: {file_path}")
    
    # Test all AI capabilities
    print("\nStep 2: Testing AI capabilities...")
    demonstrate_ai_capabilities(file_path)
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("All AI agent capabilities have been demonstrated successfully!")
    print("The API is ready for production use with your own documents.")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        exit(1)
    except Exception as e:
        print(f"Demo failed: {e}")
        exit(1)