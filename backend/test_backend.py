#!/usr/bin/env python3
"""Test script for backend functionality."""

import requests
import json
import time
import sys
from pathlib import Path


BASE_URL = "http://127.0.0.1:5000"


def test_health_check():
    """Test health check endpoint."""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed: {data}")
            return True
        else:
            print(f"✗ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend. Is it running?")
        return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False


def test_model_status():
    """Test model status endpoint."""
    print("\nTesting model status...")
    try:
        response = requests.get(f"{BASE_URL}/models/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Model status: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"✗ Model status failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Model status error: {e}")
        return False


def test_training_forms():
    """Test training forms endpoint."""
    print("\nTesting training forms...")
    try:
        response = requests.get(f"{BASE_URL}/training/forms")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Available forms: {len(data.get('forms', []))}")
            for form in data.get('forms', []):
                print(f"  - {form['name']} ({form['difficulty']})")
            return True
        else:
            print(f"✗ Training forms failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Training forms error: {e}")
        return False


def test_video_upload():
    """Test video upload (with dummy file)."""
    print("\nTesting video upload...")
    
    # Create a dummy video file for testing
    dummy_file = Path("test_video.mp4")
    if not dummy_file.exists():
        print("  Creating dummy test file...")
        with open(dummy_file, "wb") as f:
            f.write(b"dummy video content")
    
    try:
        with open(dummy_file, "rb") as f:
            files = {"video": ("test_video.mp4", f, "video/mp4")}
            response = requests.post(f"{BASE_URL}/video/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Video upload successful: {data}")
            return True, data.get('video_id')
        else:
            print(f"✗ Video upload failed with status {response.status_code}")
            return False, None
    except Exception as e:
        print(f"✗ Video upload error: {e}")
        return False, None
    finally:
        # Clean up
        if dummy_file.exists():
            dummy_file.unlink()


def test_stream_processing():
    """Test stream frame processing."""
    print("\nTesting stream processing...")
    
    # Create dummy frame data (base64 encoded image)
    dummy_frame = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCwAA8A/9k="
    
    try:
        response = requests.post(
            f"{BASE_URL}/video/stream",
            json={"frame": dummy_frame}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Stream processing successful")
            if data.get('feedback'):
                print(f"  Feedback: {data['feedback']}")
            return True
        else:
            print(f"✗ Stream processing failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Stream processing error: {e}")
        return False


def run_all_tests():
    """Run all backend tests."""
    print("=" * 50)
    print("Tai Chi Flow Backend Tests")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Model Status", test_model_status),
        ("Training Forms", test_training_forms),
        ("Stream Processing", test_stream_processing),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {test_name} crashed: {e}")
            failed += 1
        
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"Tests completed: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    # Check if backend is running
    print("Checking backend connection...")
    
    if not test_health_check():
        print("\nBackend is not running!")
        print("Please start the backend first:")
        print("  cd backend")
        print("  python app.py")
        sys.exit(1)
    
    # Run all tests
    success = run_all_tests()
    sys.exit(0 if success else 1)