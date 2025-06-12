#!/usr/bin/env python3
"""
Test script specifically for the Medium_Articles/Cursone_ai_prompt_use.pdf document
This script will diagnose and test the PDF processing capabilities.
"""

import requests
import json
from azure.storage.blob import BlobServiceClient
from config import AZURE_STORAGE_CONNECTION_STRING
import PyPDF2
import io

# API Configuration
BASE_URL = "http://localhost:5000"
PDF_PATH = "storageoneproudct/Medium_Articles/Cursone_ai_prompt_use.pdf"
PDF_URL = "https://storagetest12344.blob.core.windows.net/storageoneproudct/Medium_Articles/Cursone_ai_prompt_use.pdf"

def diagnose_pdf():
    """Diagnose the PDF file directly"""
    print("Diagnosing PDF file...")
    
    try:
        # Connect to Azure Storage
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(
            container="storageoneproudct", 
            blob="Medium_Articles/Cursone_ai_prompt_use.pdf"
        )
        
        # Download the PDF
        print("Downloading PDF from Azure Storage...")
        blob_data = blob_client.download_blob()
        content = blob_data.readall()
        print(f"Downloaded PDF: {len(content)} bytes")
        
        # Analyze PDF structure
        pdf_file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        print(f"PDF Pages: {len(pdf_reader.pages)}")
        print(f"PDF Encrypted: {pdf_reader.is_encrypted}")
        
        # Try to extract text from first few pages
        for i in range(min(3, len(pdf_reader.pages))):
            page = pdf_reader.pages[i]
            page_text = page.extract_text()
            print(f"Page {i+1} text length: {len(page_text)} characters")
            if page_text.strip():
                print(f"Sample text from page {i+1}: {page_text[:200]}...")
                return True
        
        print("No extractable text found in any pages")
        return False
        
    except Exception as e:
        print(f"Error diagnosing PDF: {e}")
        return False

def test_api_endpoint(endpoint, data, timeout=60):
    """Test a specific API endpoint"""
    api_keys = {
        "/summarize": "summarize-key-123",
        "/sentiment": "sentiment-key-123",
        "/extract-keywords": "keywords-key-123",
        "/translate": "translate-key-123",
        "/structure-data": "structure-key-123",
        "/detect-topics": "topics-key-123"
    }
    
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_keys[endpoint]
    }
    
    try:
        print(f"Testing {endpoint} endpoint...")
        response = requests.post(url, json=data, headers=headers, timeout=timeout)
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        if response.status_code == 200:
            print("SUCCESS")
            return result
        else:
            print(f"ERROR: {result.get('error', 'Unknown error')}")
            print(f"Message: {result.get('message', 'No message')}")
            return None
            
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def main():
    """Main test function"""
    print("Testing PDF Document Processing")
    print("=" * 50)
    print(f"PDF Path: {PDF_PATH}")
    print(f"PDF URL: {PDF_URL}")
    print()
    
    # Step 1: Diagnose PDF structure
    has_text = diagnose_pdf()
    print()
    
    if not has_text:
        print("This PDF appears to be image-based or has text extraction restrictions.")
        print("The API will not be able to process this specific PDF.")
        print("For testing purposes, I recommend using a text-based PDF document.")
        return
    
    # Step 2: Test API endpoints
    test_data = {"file_path": PDF_PATH}
    
    endpoints_to_test = [
        "/summarize",
        "/sentiment", 
        "/extract-keywords"
    ]
    
    for endpoint in endpoints_to_test:
        print("-" * 30)
        result = test_api_endpoint(endpoint, test_data, timeout=90)
        if result:
            # Display relevant results
            if endpoint == "/summarize" and "data" in result:
                summary = result["data"].get("summary", "")
                print(f"Summary: {summary[:300]}...")
            elif endpoint == "/sentiment" and "data" in result:
                sentiment = result["data"].get("sentiment")
                confidence = result["data"].get("confidence")
                print(f"Sentiment: {sentiment} (confidence: {confidence})")
            elif endpoint == "/extract-keywords" and "data" in result:
                keywords = result["data"].get("keywords", [])
                print(f"Keywords: {', '.join(keywords[:10])}")
        print()

if __name__ == "__main__":
    main()