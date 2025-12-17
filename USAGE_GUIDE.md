# RAG Security Scanner - Complete Usage Guide

## Table of Contents
- [Quick Start](#quick-start)
- [Request Methods](#request-methods)
- [Parameter Specification](#parameter-specification)
- [Request File Formats](#request-file-formats)
- [API Format Detection](#api-format-detection)
- [Advanced Examples](#advanced-examples)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Demo Mode
```bash
# Run a demo scan to see how it works
python src/rag_scanner.py --demo
```

### Basic Scan
```bash
# Scan a single endpoint
python src/rag_scanner.py --url https://api.example.com/chat --api-key YOUR_KEY
```

## Request Methods

### POST Requests (Default)

The scanner uses POST by default, which is suitable for most AI/LLM APIs:

```bash
python src/rag_scanner.py \
    --url https://api.example.com/chat \
    --method POST \
    --param prompt
```

### GET Requests

For search or query APIs that use GET:

```bash
python src/rag_scanner.py \
    --url https://api.example.com/search \
    --method GET \
    --param query
```

### Other Methods

The scanner also supports PUT and PATCH:

```bash
python src/rag_scanner.py \
    --url https://api.example.com/update \
    --method PUT \
    --param content
```

## Parameter Specification

### Simple Parameter

Place the payload in a top-level parameter:

```bash
python src/rag_scanner.py \
    --url https://api.example.com/chat \
    --param user_message
```

This sends: `{"user_message": "PAYLOAD"}`

### Nested Parameters (Dot Notation)

For nested JSON structures, use dot notation:

```bash
python src/rag_scanner.py \
    --url https://api.example.com/chat \
    --param messages.0.content
```

This sends:
```json
{
  "messages": [
    {
      "content": "PAYLOAD"
    }
  ]
}
```

### Additional Parameters

Add extra parameters to your requests:

```bash
python src/rag_scanner.py \
    --url https://api.example.com/chat \
    --param prompt \
    --body-param model=gpt-4 \
    --body-param temperature=0.7 \
    --body-param max_tokens=150
```

This sends:
```json
{
  "prompt": "PAYLOAD",
  "model": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 150
}
```

### Custom Headers

Add custom headers to your requests:

```bash
python src/rag_scanner.py \
    --url https://api.example.com/chat \
    --param prompt \
    --header "X-API-Version=2.0" \
    --header "X-Custom-ID=test-123"
```

## Request File Formats

### Format 1: Simple URL List

Create a text file with one URL per line:

**File: `my_endpoints.txt`**
```text
# Comment lines start with #
POST https://api.example.com/chat
GET https://api.example.com/search
https://api.openai.com/v1/chat/completions
```

**Usage:**
```bash
python src/rag_scanner.py --request-file my_endpoints.txt
```

### Format 2: JSON Configuration

For full control over request parameters:

**File: `my_requests.json`**
```json
[
  {
    "method": "POST",
    "url": "https://api.example.com/chat",
    "param_name": "user_input",
    "api_format": "generic",
    "headers": {
      "Content-Type": "application/json",
      "X-API-Key": "your-key"
    },
    "additional_params": {
      "model": "gpt-4",
      "temperature": 0.7,
      "max_tokens": 200
    }
  },
  {
    "method": "GET",
    "url": "https://api.example.com/search",
    "param_name": "query",
    "additional_params": {
      "limit": 10,
      "format": "json"
    }
  }
]
```

**Usage:**
```bash
python src/rag_scanner.py --request-file my_requests.json
```

### Format 3: Raw HTTP Request

Copy/paste actual HTTP requests:

**File: `my_http_requests.txt`**
```http
POST https://api.example.com/chat HTTP/1.1
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
  "prompt": "PAYLOAD",
  "model": "gpt-3.5-turbo",
  "max_tokens": 150
}


GET https://api.example.com/search?format=json HTTP/1.1
Accept: application/json
X-API-Key: YOUR_KEY
```

**Note:** Separate multiple requests with triple newlines (`\n\n\n`)

**Usage:**
```bash
python src/rag_scanner.py --request-file my_http_requests.txt
```

## API Format Detection

### Auto Detection (Default)

The scanner automatically detects common API formats:

```bash
python src/rag_scanner.py \
    --url https://api.openai.com/v1/chat/completions \
    --api-format auto
```

### OpenAI Format

For OpenAI-compatible APIs:

```bash
python src/rag_scanner.py \
    --url https://api.openai.com/v1/chat/completions \
    --api-format openai \
    --body-param model=gpt-3.5-turbo \
    --body-param max_tokens=150
```

Sends:
```json
{
  "model": "gpt-3.5-turbo",
  "messages": [{"role": "user", "content": "PAYLOAD"}],
  "max_tokens": 150
}
```

### Generic Format

For custom APIs:

```bash
python src/rag_scanner.py \
    --url https://custom-api.example.com/generate \
    --api-format generic \
    --param prompt
```

Sends:
```json
{
  "prompt": "PAYLOAD"
}
```

## Advanced Examples

### Example 1: OpenAI Chat API

```bash
python src/rag_scanner.py \
    --url https://api.openai.com/v1/chat/completions \
    --api-key sk-your-openai-key \
    --method POST \
    --api-format openai \
    --body-param model=gpt-3.5-turbo \
    --body-param max_tokens=150 \
    --scan-type full \
    --format html \
    --delay 2.0
```

### Example 2: Custom RAG System (POST)

```bash
python src/rag_scanner.py \
    --url https://my-rag-system.com/ask \
    --method POST \
    --param question \
    --body-param context_enabled=true \
    --body-param max_results=5 \
    --header "X-RAG-Version=1.0" \
    --scan-type prompt
```

### Example 3: Search API (GET)

```bash
python src/rag_scanner.py \
    --url https://search-api.example.com/query \
    --method GET \
    --param q \
    --body-param limit=10 \
    --body-param sort=relevance \
    --scan-type data
```

### Example 4: HuggingFace Inference API

```bash
python src/rag_scanner.py \
    --url https://api-inference.huggingface.co/models/gpt2 \
    --method POST \
    --param inputs \
    --header "Authorization=Bearer hf_YOUR_TOKEN" \
    --body-param max_length=100 \
    --delay 3.0 \
    --scan-type full
```

### Example 5: Multiple Endpoints with Different Configs

**File: `multi_endpoint.json`**
```json
[
  {
    "method": "POST",
    "url": "https://api1.example.com/chat",
    "param_name": "message",
    "additional_params": {"model": "gpt-4"}
  },
  {
    "method": "GET",
    "url": "https://api2.example.com/search",
    "param_name": "query",
    "additional_params": {"limit": 5}
  },
  {
    "method": "POST",
    "url": "https://api3.example.com/ask",
    "param_name": "question",
    "additional_params": {"use_rag": true}
  }
]
```

**Run:**
```bash
python src/rag_scanner.py \
    --request-file multi_endpoint.json \
    --scan-type full \
    --format html \
    --delay 1.5
```

### Example 6: Testing Different Parameters

Test the same endpoint with different parameter names:

**File: `param_tests.json`**
```json
[
  {
    "method": "POST",
    "url": "https://api.example.com/chat",
    "param_name": "prompt"
  },
  {
    "method": "POST",
    "url": "https://api.example.com/chat",
    "param_name": "user_input"
  },
  {
    "method": "POST",
    "url": "https://api.example.com/chat",
    "param_name": "message"
  }
]
```

```bash
python src/rag_scanner.py --request-file param_tests.json
```

## Scan Types

### Full Scan (Default)
Tests all vulnerability categories:
```bash
python src/rag_scanner.py --url URL --scan-type full
```

### Prompt Injection Only
```bash
python src/rag_scanner.py --url URL --scan-type prompt
```

### Data Leakage Only
```bash
python src/rag_scanner.py --url URL --scan-type data
```

### Function Abuse Only
```bash
python src/rag_scanner.py --url URL --scan-type function
```

### Context Manipulation Only
```bash
python src/rag_scanner.py --url URL --scan-type context
```

## Output Formats

### JSON Report
```bash
python src/rag_scanner.py --url URL --format json --output report.json
```

### HTML Report
```bash
python src/rag_scanner.py --url URL --format html --output report.html
```

### Both Formats
```bash
python src/rag_scanner.py --url URL --format json
python src/rag_scanner.py --url URL --format html
```

## Troubleshooting

### Issue: Connection Timeout

**Solution:** Increase timeout value:
```bash
python src/rag_scanner.py --url URL --timeout 60
```

### Issue: Rate Limiting

**Solution:** Increase delay between requests:
```bash
python src/rag_scanner.py --url URL --delay 3.0
```

### Issue: Authentication Errors

**Solution:** Add proper headers and API key:
```bash
python src/rag_scanner.py \
    --url URL \
    --api-key YOUR_KEY \
    --header "X-Custom-Auth=token123"
```

### Issue: Wrong Parameter Name

**Solution:** Specify the correct parameter:
```bash
python src/rag_scanner.py --url URL --param correct_param_name
```

### Issue: Nested JSON Required

**Solution:** Use dot notation:
```bash
python src/rag_scanner.py --url URL --param data.query.text
```

### Issue: Request File Not Parsed

**Solution:** Check file format and syntax:
```bash
# Validate JSON
cat my_requests.json | python -m json.tool

# Check file encoding
file my_requests.txt
```

## Best Practices

1. **Start with Demo Mode**: Always test with `--demo` first to understand the output
2. **Use Request Files**: For complex configurations, use JSON request files
3. **Set Appropriate Delays**: Respect API rate limits with `--delay`
4. **Save Both Formats**: Generate both JSON and HTML reports for different uses
5. **Test Incrementally**: Start with `--scan-type prompt`, then expand to `full`
6. **Review Logs**: Use `--verbose` for detailed debugging information
7. **Backup Configs**: Keep your request files in version control
8. **Document Custom APIs**: Add comments in request files to explain custom parameters

## API-Specific Tips

### For OpenAI API
- Use `--api-format openai`
- Set model with `--body-param model=gpt-3.5-turbo`
- Increase delay to avoid rate limits: `--delay 2.0`

### For HuggingFace
- Increase timeout: `--timeout 60`
- Increase delay: `--delay 3.0`
- Use proper model URL in `--url`

### For Custom RAG Systems
- Test with `--method POST` and `--method GET`
- Try different param names: `prompt`, `query`, `question`, `user_input`
- Add custom headers as needed
- Use `--api-format generic` or `--api-format custom`

### For Search APIs
- Use `--method GET`
- Common param names: `q`, `query`, `search`, `term`
- Add pagination params: `--body-param limit=10 --body-param offset=0`

## Environment Variables

You can use environment variables instead of command-line arguments:

```bash
export TARGET_URL="https://api.example.com/chat"
export OPENAI_API_KEY="sk-your-key"

python src/rag_scanner.py --scan-type full
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/olegnazarov/rag-security-scanner/issues
- Documentation: See README.md
- Examples: Check `examples/` directory
