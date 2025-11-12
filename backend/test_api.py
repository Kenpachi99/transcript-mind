"""
Test script for TranscriptMind API
Run this after starting the server to verify all endpoints work correctly.
"""
import requests
import json
import time
from typing import Dict, Any


BASE_URL = "http://localhost:8000"

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_test(test_name: str):
    """Print test header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}TEST: {test_name}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")


def print_success(message: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message: str):
    """Print error message."""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_info(message: str):
    """Print info message."""
    print(f"{Colors.YELLOW}ℹ {message}{Colors.END}")


def test_health_check() -> bool:
    """Test the health check endpoint."""
    print_test("Health Check")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print_success("Health check passed!")
                return True
            else:
                print_error("Server responded but status is not healthy")
                return False
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print_error("Could not connect to server. Is it running?")
        print_info("Start the server with: cd backend && ./run.sh")
        return False
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False


def test_transcription(youtube_url: str) -> Dict[str, Any]:
    """Test video transcription endpoint."""
    print_test("Video Transcription")

    print_info(f"Transcribing: {youtube_url}")
    print_info("This may take a minute depending on video length...")

    try:
        start_time = time.time()

        response = requests.post(
            f"{BASE_URL}/transcribe",
            json={"youtube_url": youtube_url},
            timeout=300  # 5 minute timeout for longer videos
        )

        elapsed_time = time.time() - start_time

        print(f"Status Code: {response.status_code}")
        print(f"Time taken: {elapsed_time:.2f} seconds")

        if response.status_code == 200:
            data = response.json()

            print(f"\n{Colors.BOLD}Transcription Result:{Colors.END}")
            print(f"Transcript ID: {data.get('transcript_id')}")
            print(f"Language: {data.get('language')}")
            print(f"Duration: {data.get('duration')} seconds")
            print(f"Status: {data.get('status')}")

            # Print first 200 characters of transcript
            transcript = data.get('transcript', '')
            print(f"\n{Colors.BOLD}Transcript Preview:{Colors.END}")
            print(f"{transcript[:200]}...")

            print_success("Transcription completed successfully!")
            return data
        else:
            print_error(f"Transcription failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return {}

    except requests.exceptions.Timeout:
        print_error("Request timed out. Video might be too long.")
        return {}
    except Exception as e:
        print_error(f"Transcription failed: {str(e)}")
        return {}


def test_get_transcript(transcript_id: str) -> bool:
    """Test retrieving a transcript by ID."""
    print_test("Retrieve Transcript by ID")

    print_info(f"Fetching transcript: {transcript_id}")

    try:
        response = requests.get(f"{BASE_URL}/transcript/{transcript_id}", timeout=5)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            print(f"\n{Colors.BOLD}Retrieved Transcript:{Colors.END}")
            print(f"URL: {data.get('url')}")
            print(f"Language: {data.get('language')}")
            print(f"Duration: {data.get('duration')} seconds")

            transcript = data.get('transcript', '')
            print(f"\n{Colors.BOLD}Transcript Preview:{Colors.END}")
            print(f"{transcript[:200]}...")

            print_success("Transcript retrieved successfully!")
            return True
        elif response.status_code == 404:
            print_error("Transcript not found")
            return False
        else:
            print_error(f"Failed to retrieve transcript: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Failed to retrieve transcript: {str(e)}")
        return False


def test_invalid_url() -> bool:
    """Test error handling with invalid URL."""
    print_test("Error Handling - Invalid URL")

    invalid_url = "https://invalid-url-that-does-not-exist.com"
    print_info(f"Testing with invalid URL: {invalid_url}")

    try:
        response = requests.post(
            f"{BASE_URL}/transcribe",
            json={"youtube_url": invalid_url},
            timeout=30
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code >= 400:
            print_success("Server correctly handled invalid URL with error response")
            print(f"Error message: {response.json().get('detail', 'No detail provided')}")
            return True
        else:
            print_error("Server should have returned an error for invalid URL")
            return False

    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("="*60)
    print("  TranscriptMind API Test Suite")
    print("="*60)
    print(f"{Colors.END}\n")

    results = []

    # Test 1: Health Check
    results.append(("Health Check", test_health_check()))

    if not results[0][1]:
        print_error("\nServer is not running. Cannot continue with other tests.")
        print_info("Start the server with: cd backend && ./run.sh")
        return

    # Test 2: Transcribe a short video
    # Using "Me at the zoo" - first YouTube video (19 seconds)
    short_video_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    transcript_data = test_transcription(short_video_url)
    results.append(("Transcription", bool(transcript_data)))

    # Test 3: Retrieve transcript (if transcription succeeded)
    if transcript_data:
        transcript_id = transcript_data.get('transcript_id')
        if transcript_id:
            results.append(("Retrieve Transcript", test_get_transcript(transcript_id)))

    # Test 4: Error handling
    results.append(("Error Handling", test_invalid_url()))

    # Print summary
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("="*60)
    print("  TEST SUMMARY")
    print("="*60)
    print(f"{Colors.END}\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = f"{Colors.GREEN}PASSED{Colors.END}" if result else f"{Colors.RED}FAILED{Colors.END}"
        print(f"  {test_name}: {status}")

    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests passed{Colors.END}\n")

    if passed == total:
        print_success("All tests passed! 🎉")
    else:
        print_error(f"{total - passed} test(s) failed")


if __name__ == "__main__":
    main()
