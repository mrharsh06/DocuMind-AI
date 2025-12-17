import requests
import os
import time
from typing import Optional

BASE_URL="http://localhost:8000"

def test_health_check():
    print("\n🔍 Testing health check...")
    response=requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_upload_document(file_path: str):
    """Test document upload endpoint"""
    print(f"\n📄 Testing document upload: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None
    
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/documents/upload", files=files)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Upload successful!")
        print(f"   File: {result.get('file_name')}")
        print(f"   Chunks: {result.get('chunk_count')}")
        return result.get('file_name')
    else:
        print(f"❌ Upload failed: {response.text}")
        return None
def test_query(question: str, n_results: int = 5,file_name: Optional[str]=None):
    """Test query endpoint"""
    print(f"\n❓ Testing query: '{question}'")

    if file_name:
        print(f"   Filtering to file: {file_name}")
    
    payload = {
        "question": question,
        "n_results": n_results
    }
    if file_name:
        payload["file_name"]=file_name
    
    response = requests.post(f"{BASE_URL}/query/", json=payload)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Query successful!")
        print(f"\n📝 Answer:")
        print(f"   {result.get('answer')}")
        print(f"\n📚 Sources found: {len(result.get('sources', []))}")
        for i, source in enumerate(result.get('sources', [])[:3], 1):
            print(f"\n   Source {i}:")
            print(f"   - File: {source.get('file_name')}")
            print(f"   - Similarity: {source.get('similarity_score'):.3f}")
            print(f"   - Preview: {source.get('chunk')[:100]}...")
        return result
    else:
        print(f"❌ Query failed: {response.text}")
        return None
def test_query_with_file_filter(question: str,file_name: str):
    """Test query endpoint with file name filter"""
    print(f"\n🔍 Testing query with file filter: '{question}'")
    print(f"   Filtering to: {file_name}")
    
    payload = {
        "question": question,
        "n_results": 5,
        "file_name": file_name
    }
    
    response = requests.post(f"{BASE_URL}/query/", json=payload)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Filtered query successful!")
        print(f"\n📝 Answer:")
        print(f"   {result.get('answer')}")
        print(f"\n📚 Sources found: {len(result.get('sources', []))}")
        
        # Check if all sources are from the filtered file
        all_from_filtered_file = all(
            source.get('file_name') == file_name 
            for source in result.get('sources', [])
        )
        
        if all_from_filtered_file:
            print(f"✅ All sources are from '{file_name}' (filter working!)")
        else:
            print(f"⚠️  Some sources are not from '{file_name}' (filter may not be working)")
        
        for i, source in enumerate(result.get('sources', [])[:3], 1):
            print(f"\n   Source {i}:")
            print(f"   - File: {source.get('file_name')}")
            print(f"   - Similarity: {source.get('similarity_score'):.3f}")
            print(f"   - Preview: {source.get('chunk')[:100]}...")
        return result
    else:
        print(f"❌ Filtered query failed: {response.text}")
        return None

def test_list_documents():
    """Test admin list documents endpoint"""
    print(f"\n📋 Testing list documents...")
    
    response = requests.get(f"{BASE_URL}/admin/documents")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ List successful!")
        print(f"   Total chunks: {result.get('total_count')}")
        print(f"   Unique files: {result.get('unique_files')}")
        print(f"\n   Files:")
        for file_info in result.get('files', []):
            print(f"   - {file_info.get('file_name')}: {file_info.get('chunk_count')} chunks")
        return result
    else:
        print(f"❌ List failed: {response.text}")
        return None
def test_statistics():
    """Test admin statistics endpoint"""
    print(f"\n📊 Testing statistics...")
    
    response = requests.get(f"{BASE_URL}/admin/statistics")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Statistics successful!")
        print(f"   Total chunks: {result.get('total_chunks')}")
        print(f"   Unique files: {result.get('unique_files')}")
        return result
    else:
        print(f"❌ Statistics failed: {response.text}")
        return None
def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 DocuMind AI - System Test Script")
    print("=" * 60)
    
    # Step 1: Health check
    if not test_health_check():
        print("\n❌ API is not running! Please start the server with: uvicorn app.main:app --reload")
        return
    
    # Step 2: List documents (before upload)
    print("\n" + "-" * 60)
    test_list_documents()
    
    # Step 3: Upload a test document (if you have one)
    print("\n" + "-" * 60)
    # You can change this path to your test document
    test_file = "test.txt"  # Change this to your test file path
    uploaded_file = None
    
    if os.path.exists(test_file):
        uploaded_file = test_upload_document(test_file)
        # Wait a bit for processing
        time.sleep(2)
    else:
        print(f"\n⚠️  Test file '{test_file}' not found. Skipping upload test.")
        print("   You can create a simple test.txt file or use an existing document.")
    
    # Step 4: Query (only if we have documents)
    print("\n" + "-" * 60)
    if uploaded_file:
        test_query("What is this document about?")
    else:
        # Try to query any existing documents
        all_docs = test_list_documents()
        if all_docs and all_docs.get('files'):
            test_query("What is this document about?")
        else:
            print("\n⚠️  Skipping query test (no documents available)")
    
    # Step 5: List documents (after upload)
    print("\n" + "-" * 60)
    test_list_documents()
    
    # Step 6: Statistics
    print("\n" + "-" * 60)
    test_statistics()
    
    print("\n" + "=" * 60)
    print("✅ Test script completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()