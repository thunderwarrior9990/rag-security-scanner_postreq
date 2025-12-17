#!/bin/bash
# CLI Test Script for RAG Security Scanner Enhancements
# Tests various command-line configurations

echo "=========================================="
echo "RAG Security Scanner - CLI Tests"
echo "=========================================="
echo ""

# Test 1: Demo mode
echo "Test 1: Demo Mode"
python3 src/rag_scanner.py --demo --scan-type prompt --delay 0.1 --format json
if [ $? -eq 0 ]; then
    echo "✓ Test 1 passed: Demo mode works"
else
    echo "✗ Test 1 failed"
fi
echo ""

# Test 2: POST with custom parameter
echo "Test 2: POST Request with Custom Parameter"
python3 src/rag_scanner.py \
    --demo \
    --method POST \
    --param user_message \
    --body-param model=gpt-4 \
    --scan-type prompt \
    --delay 0.1
if [ $? -eq 0 ]; then
    echo "✓ Test 2 passed: POST with custom param"
else
    echo "✗ Test 2 failed"
fi
echo ""

# Test 3: GET request
echo "Test 3: GET Request"
python3 src/rag_scanner.py \
    --demo \
    --method GET \
    --param query \
    --body-param limit=10 \
    --scan-type prompt \
    --delay 0.1
if [ $? -eq 0 ]; then
    echo "✓ Test 3 passed: GET request works"
else
    echo "✗ Test 3 failed"
fi
echo ""

# Test 4: Custom headers
echo "Test 4: Custom Headers"
python3 src/rag_scanner.py \
    --demo \
    --method POST \
    --param prompt \
    --header "X-API-Version=2.0" \
    --header "X-Custom=test" \
    --scan-type prompt \
    --delay 0.1
if [ $? -eq 0 ]; then
    echo "✓ Test 4 passed: Custom headers work"
else
    echo "✗ Test 4 failed"
fi
echo ""

# Test 5: Request file (simple)
echo "Test 5: Simple Request File"
python3 src/rag_scanner.py \
    --request-file examples/requests_simple.txt \
    --scan-type prompt \
    --delay 0.1
if [ $? -eq 0 ]; then
    echo "✓ Test 5 passed: Simple request file works"
else
    echo "✗ Test 5 failed"
fi
echo ""

# Test 6: Request file (JSON)
echo "Test 6: JSON Request File"
python3 src/rag_scanner.py \
    --request-file examples/requests_json.json \
    --scan-type prompt \
    --delay 0.1
if [ $? -eq 0 ]; then
    echo "✓ Test 6 passed: JSON request file works"
else
    echo "✗ Test 6 failed"
fi
echo ""

# Test 7: Different API formats
echo "Test 7: API Format Specification"
python3 src/rag_scanner.py \
    --demo \
    --method POST \
    --param prompt \
    --api-format openai \
    --body-param model=gpt-3.5-turbo \
    --scan-type prompt \
    --delay 0.1
if [ $? -eq 0 ]; then
    echo "✓ Test 7 passed: API format works"
else
    echo "✗ Test 7 failed"
fi
echo ""

# Test 8: Multiple body parameters
echo "Test 8: Multiple Body Parameters"
python3 src/rag_scanner.py \
    --demo \
    --method POST \
    --param prompt \
    --body-param model=gpt-4 \
    --body-param temperature=0.7 \
    --body-param max_tokens=150 \
    --scan-type prompt \
    --delay 0.1
if [ $? -eq 0 ]; then
    echo "✓ Test 8 passed: Multiple body params work"
else
    echo "✗ Test 8 failed"
fi
echo ""

# Test 9: HTML output
echo "Test 9: HTML Report Generation"
python3 src/rag_scanner.py \
    --demo \
    --scan-type prompt \
    --format html \
    --delay 0.1
if [ $? -eq 0 ]; then
    echo "✓ Test 9 passed: HTML report generation works"
else
    echo "✗ Test 9 failed"
fi
echo ""

echo "=========================================="
echo "All CLI tests completed!"
echo "=========================================="
