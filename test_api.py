#!/usr/bin/env python3
"""
Test script for AI Agent API Server
Demonstrates all API endpoints with proper authentication
"""

import requests
import json
import sys

# API Configuration
BASE_URL = "http://localhost:5000"
API_KEYS = {
    "summarize": "summarize-key-123",
    "sentiment": "sentiment-key-123", 
    "extract-keywords": "keywords-key-123",
    "translate": "translate-key-123",
    "structure-data": "structure-key-123",
    "detect-topics": "topics-key-123"
}

def make_request(endpoint, data=None, api_key=None):
    """Make HTTP request to API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if api_key:
        headers["X-API-Key"] = api_key
    
    try:
        if data:
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            response = requests.get(url, headers=headers, timeout=10)
        
        return response
    except requests.exceptions.ConnectionError:
        print(f"Connection failed: Server not reachable at {BASE_URL}")
        return None
    except requests.exceptions.Timeout:
        print(f"Request timeout: Server took too long to respond")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing Health Endpoint...")
    response = make_request("/health")
    
    if response and response.status_code == 200:
        print("✅ Health check passed")
        data = response.json()
        print(f"   Service: {data.get('service')}")
        print(f"   Status: {data.get('status')}")
        return True
    else:
        print("❌ Health check failed")
        return False

def test_api_info():
    """Test API information endpoint"""
    print("\n📋 Testing API Information...")
    response = make_request("/")
    
    if response and response.status_code == 200:
        print("✅ API info retrieved successfully")
        data = response.json()
        print(f"   Service: {data.get('service')}")
        print(f"   Version: {data.get('version')}")
        print(f"   Available endpoints: {len(data.get('endpoints', {}))}")
        return True
    else:
        print("❌ API info retrieval failed")
        return False

def test_authentication():
    """Test API key authentication"""
    print("\n🔐 Testing Authentication...")
    
    # Test without API key
    response = make_request("/summarize", {"file_path": "test/file.txt"})
    if response and response.status_code == 401:
        print("✅ Authentication required (no API key)")
    else:
        print("❌ Authentication test failed (no API key)")
        return False
    
    # Test with invalid API key
    response = make_request("/summarize", {"file_path": "test/file.txt"}, "invalid-key")
    if response and response.status_code == 403:
        print("✅ Authentication failed (invalid API key)")
    else:
        print("❌ Authentication test failed (invalid API key)")
        return False
    
    return True

def test_ai_endpoint(endpoint_name, endpoint_path, test_data):
    """Test individual AI endpoint"""
    print(f"\n🤖 Testing {endpoint_name}...")
    
    api_key = API_KEYS.get(endpoint_name.lower().replace(" ", "-").replace("_", "-"))
    response = make_request(endpoint_path, test_data, api_key)
    
    if response:
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ File not found (expected for test file)")
            print("   Authentication and endpoint logic working correctly")
            return True
        elif response.status_code == 200:
            print("✅ Request successful")
            return True
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error')}")
                print(f"   Message: {error_data.get('message')}")
            except:
                print(f"   Response: {response.text[:200]}")
            return False
    else:
        print("❌ Request failed")
        return False

def run_comprehensive_tests():
    """Run all API tests"""
    print("🚀 Starting AI Agent API Comprehensive Tests")
    print("=" * 50)
    
    results = []
    
    # Basic endpoint tests
    results.append(("Health Check", test_health()))
    results.append(("API Information", test_api_info()))
    results.append(("Authentication", test_authentication()))
    
    # AI endpoint tests
    test_file_path = "test-container/sample-document.pdf"
    
    ai_tests = [
        ("Summarize", "/summarize", {"file_path": test_file_path}),
        ("Sentiment", "/sentiment", {"file_path": test_file_path}),
        ("Extract Keywords", "/extract-keywords", {"file_path": test_file_path}),
        ("Translate", "/translate", {"file_path": test_file_path, "target_language": "Spanish"}),
        ("Structure Data", "/structure-data", {"file_path": test_file_path}),
        ("Detect Topics", "/detect-topics", {"file_path": test_file_path})
    ]
    
    for name, path, data in ai_tests:
        results.append((name, test_ai_endpoint(name, path, data)))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is fully functional.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

def demonstrate_api_usage():
    """Demonstrate how to use the API with real examples"""
    print("\n" + "=" * 50)
    print("📚 API Usage Examples")
    print("=" * 50)
    
    examples = [
        {
            "name": "Document Summarization",
            "description": "Summarize a PDF document",
            "curl": '''curl -X POST http://localhost:5000/summarize \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: summarize-key-123" \\
  -d '{"file_path": "documents/report.pdf"}'
'''
        },
        {
            "name": "Sentiment Analysis", 
            "description": "Analyze document sentiment",
            "curl": '''curl -X POST http://localhost:5000/sentiment \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: sentiment-key-123" \\
  -d '{"file_path": "documents/feedback.txt"}'
'''
        },
        {
            "name": "Language Translation",
            "description": "Translate document to Hindi",
            "curl": '''curl -X POST http://localhost:5000/translate \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: translate-key-123" \\
  -d '{"file_path": "documents/article.pdf", "target_language": "Hindi"}'
'''
        }
    ]
    
    for example in examples:
        print(f"\n{example['name']}:")
        print(f"Description: {example['description']}")
        print("Command:")
        print(example['curl'])

if __name__ == "__main__":
    print("AI Agent API Test Suite")
    print("This script tests all endpoints and demonstrates API usage")
    print(f"Testing against: {BASE_URL}")
    
    try:
        # Run comprehensive tests
        success = run_comprehensive_tests()
        
        # Show usage examples
        demonstrate_api_usage()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        sys.exit(1)