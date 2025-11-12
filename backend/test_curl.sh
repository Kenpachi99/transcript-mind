#!/bin/bash

# Simple curl-based test script for TranscriptMind API
# Requires: curl, jq (for JSON formatting)

BASE_URL="http://localhost:8000"
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  TranscriptMind API - Curl Tests${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Test 1: Health Check
echo -e "${BLUE}[TEST 1] Health Check${NC}"
echo "Request: GET $BASE_URL/health"
echo ""

HEALTH_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/health")
HTTP_STATUS=$(echo "$HEALTH_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
RESPONSE_BODY=$(echo "$HEALTH_RESPONSE" | sed '/HTTP_STATUS/d')

if [ "$HTTP_STATUS" = "200" ]; then
    echo -e "${GREEN}✓ Status: $HTTP_STATUS${NC}"
    echo "Response:"
    if command -v jq &> /dev/null; then
        echo "$RESPONSE_BODY" | jq .
    else
        echo "$RESPONSE_BODY"
    fi
else
    echo -e "${RED}✗ Status: $HTTP_STATUS${NC}"
    echo -e "${RED}Server might not be running. Start it with: ./run.sh${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Press Enter to continue to transcription test...${NC}"
read

# Test 2: Transcribe a short video
echo -e "\n${BLUE}[TEST 2] Transcribe YouTube Video${NC}"
echo "Request: POST $BASE_URL/transcribe"
echo "Video: https://www.youtube.com/watch?v=jNQXAC9IVRw (Me at the zoo - 19 seconds)"
echo -e "${YELLOW}Note: This will take about 30-60 seconds...${NC}\n"

TRANSCRIBE_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X POST "$BASE_URL/transcribe" \
    -H "Content-Type: application/json" \
    -d '{
        "youtube_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    }')

HTTP_STATUS=$(echo "$TRANSCRIBE_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
RESPONSE_BODY=$(echo "$TRANSCRIBE_RESPONSE" | sed '/HTTP_STATUS/d')

if [ "$HTTP_STATUS" = "200" ]; then
    echo -e "${GREEN}✓ Status: $HTTP_STATUS${NC}"
    echo "Response:"
    if command -v jq &> /dev/null; then
        echo "$RESPONSE_BODY" | jq .
        TRANSCRIPT_ID=$(echo "$RESPONSE_BODY" | jq -r '.transcript_id')
    else
        echo "$RESPONSE_BODY"
        TRANSCRIPT_ID=$(echo "$RESPONSE_BODY" | grep -o '"transcript_id":"[^"]*"' | cut -d'"' -f4)
    fi
else
    echo -e "${RED}✗ Status: $HTTP_STATUS${NC}"
    echo "Response: $RESPONSE_BODY"
    exit 1
fi

echo ""
echo -e "${YELLOW}Press Enter to retrieve the transcript...${NC}"
read

# Test 3: Retrieve transcript
if [ ! -z "$TRANSCRIPT_ID" ]; then
    echo -e "\n${BLUE}[TEST 3] Retrieve Transcript${NC}"
    echo "Request: GET $BASE_URL/transcript/$TRANSCRIPT_ID"
    echo ""

    RETRIEVE_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$BASE_URL/transcript/$TRANSCRIPT_ID")
    HTTP_STATUS=$(echo "$RETRIEVE_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
    RESPONSE_BODY=$(echo "$RETRIEVE_RESPONSE" | sed '/HTTP_STATUS/d')

    if [ "$HTTP_STATUS" = "200" ]; then
        echo -e "${GREEN}✓ Status: $HTTP_STATUS${NC}"
        echo "Response:"
        if command -v jq &> /dev/null; then
            echo "$RESPONSE_BODY" | jq .
        else
            echo "$RESPONSE_BODY"
        fi
    else
        echo -e "${RED}✗ Status: $HTTP_STATUS${NC}"
        echo "Response: $RESPONSE_BODY"
    fi
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ All tests completed!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Tip: For better JSON formatting, install jq:"
echo "  Ubuntu/Debian: sudo apt-get install jq"
echo "  macOS: brew install jq"
