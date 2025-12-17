# RAG Security Scanner - Quick Reference Guide

## 🚀 Quick Start

### Basic Commands

```bash
# Demo mode
python src/rag_scanner.py --demo

# Scan OpenAI API
python src/rag_scanner.py --url https://api.openai.com/v1/chat/completions --api-key YOUR_KEY

# Scan custom API
python src/rag_scanner.py --url YOUR_API_URL --method POST --param prompt
```

## 📋 Command Line Options

### Core Options
| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--url` | `-u` | Target URL | `--url https://api.example.com/chat` |
| `--api-key` | `-k` | API key | `--api-key sk-xxx` |
| `--demo` | - | Demo mode | `--demo` |

### Request Configuration
| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--method` | `-m` | HTTP method | `--method POST` or `--method GET` |
| `--param` | `-p` | Parameter name for payload | `--param user_input` |
| `--body-param` | - | Additional parameter | `--body-param model=gpt-4` |
| `--header` | - | Custom header | `--header "X-API-Version=2.0"` |
| `--api-format` | - | API format | `--api-format openai` |
| `--request-file` | `-r` | Request file path | `--request-file requests.json` |

### Scan Options
| Option | Short | Description | Values |
|--------|-------|-------------|--------|
| `--scan-type` | - | Type of scan | `full`, `prompt`, `data`, `function`, `context` |
| `--delay` | `-d` | Delay between requests | `--delay 2.0` (seconds) |
| `--timeout` | `-t` | Request timeout | `--timeout 60` (seconds) |

### Output Options
| Option | Short | Description | Values |
|--------|-------|-------------|--------|
| `--format` | `-f` | Output format | `json`, `html` |
| `--output` | `-o` | Output filename | `--output report.json` |
| `--verbose` | `-v` | Verbose output | `--verbose` |

## 📝 Common Usage Patterns

### Pattern 1: Test OpenAI-Compatible API
```bash
python src/rag_scanner.py \
    --url https://api.openai.com/v1/chat/completions \
    --api-key sk-YOUR_KEY \
    --api-format openai \
    --scan-type full \
    --delay 2.0
```

### Pattern 2: Test Custom POST API
```bash
python src/rag_scanner.py \
    --url https://api.example.com/chat \
    --method POST \
    --param user_message \
    --body-param model=gpt-4 \
    --body-param temperature=0.7 \
    --scan-type full
```

### Pattern 3: Test GET API
```bash
python src/rag_scanner.py \
    --url https://api.example.com/search \
    --method GET \
    --param query \
    --body-param limit=10 \
    --scan-type data
```

### Pattern 4: Test Multiple Endpoints
```bash
python src/rag_scanner.py \
    --request-file examples/requests_json.json \
    --scan-type full \
    --format html
```

### Pattern 5: Test with Custom Headers
```bash
python src/rag_scanner.py \
    --url https://api.example.com/ai \
    --method POST \
    --param prompt \
    --header "X-API-Version=2.0" \
    --header "Authorization=Bearer TOKEN" \
    --scan-type prompt
```

## 📁 Request File Formats

### Format 1: Simple Text File
```text
# my_urls.txt
POST https://api.example.com/chat
GET https://api.example.com/search
```

**Usage:** `--request-file my_urls.txt`

### Format 2: JSON Configuration
```json
[
  {
    "method": "POST",
    "url": "https://api.example.com/chat",
    "param_name": "prompt",
    "additional_params": {"model": "gpt-4"}
  }
]
```

**Usage:** `--request-file config.json`

### Format 3: HTTP Request
```http
POST https://api.example.com/chat HTTP/1.1
Content-Type: application/json

{"prompt": "PAYLOAD"}
```

**Usage:** `--request-file request.http`

## 🎯 Scan Types

| Type | Focus | Use Case |
|------|-------|----------|
| `full` | All vulnerabilities | Comprehensive security audit |
| `prompt` | Prompt injection | Test instruction manipulation |
| `data` | Data leakage | Test information disclosure |
| `function` | Function abuse | Test API/function misuse |
| `context` | Context manipulation | Test context poisoning |

## 🔧 Common Scenarios

### Scenario: Testing a New AI Chatbot

**Step 1:** Test with default settings
```bash
python src/rag_scanner.py --url YOUR_URL --demo --scan-type prompt
```

**Step 2:** Identify correct parameter
```bash
# Try different parameter names
python src/rag_scanner.py --url YOUR_URL --param prompt --scan-type prompt
python src/rag_scanner.py --url YOUR_URL --param message --scan-type prompt
python src/rag_scanner.py --url YOUR_URL --param user_input --scan-type prompt
```

**Step 3:** Full scan with correct config
```bash
python src/rag_scanner.py \
    --url YOUR_URL \
    --method POST \
    --param CORRECT_PARAM \
    --scan-type full \
    --format html
```

### Scenario: Testing Multiple AI Services

**Step 1:** Create JSON config file
```json
[
  {
    "method": "POST",
    "url": "https://api1.example.com/chat",
    "param_name": "prompt",
    "additional_params": {"model": "gpt-4"}
  },
  {
    "method": "POST",
    "url": "https://api2.example.com/ask",
    "param_name": "question"
  }
]
```

**Step 2:** Run scan
```bash
python src/rag_scanner.py --request-file services.json --scan-type full
```

### Scenario: Rate-Limited API

```bash
python src/rag_scanner.py \
    --url YOUR_URL \
    --delay 5.0 \
    --timeout 120 \
    --scan-type prompt
```

## 🚨 Troubleshooting

### Issue: "Connection timeout"
**Solution:** Increase timeout
```bash
--timeout 120
```

### Issue: "Rate limit exceeded"
**Solution:** Increase delay
```bash
--delay 5.0
```

### Issue: "Wrong parameter"
**Solution:** Specify correct parameter
```bash
--param correct_name
```

### Issue: "Authentication failed"
**Solution:** Add API key and headers
```bash
--api-key YOUR_KEY --header "Authorization=Bearer TOKEN"
```

## 📊 Output Files

### Automatic Naming
- JSON: `scan_YYYYMMDD_HHMMSS_HASH_report.json`
- HTML: `scan_YYYYMMDD_HHMMSS_HASH_report.html`

### Custom Naming
```bash
--output my_custom_report.json
```

## 🔐 Security Best Practices

1. **Never commit API keys** - Use environment variables
   ```bash
   export OPENAI_API_KEY="sk-xxx"
   python src/rag_scanner.py --url URL
   ```

2. **Respect rate limits** - Use appropriate delays
   ```bash
   --delay 2.0  # 2 seconds between requests
   ```

3. **Test in staging first** - Don't test production without permission

4. **Save reports** - Keep evidence of findings
   ```bash
   --format html --output report_$(date +%Y%m%d).html
   ```

5. **Review findings** - Not all detections are real vulnerabilities

## 📚 Documentation Files

- **README.md** - Project overview
- **USAGE_GUIDE.md** - Comprehensive guide
- **ENHANCEMENTS.md** - New features details
- **QUICK_REFERENCE.md** - This file
- **examples/** - Example configurations

## 💡 Tips & Tricks

### Tip 1: Test incrementally
```bash
# Start small
--scan-type prompt --delay 0.5

# Then expand
--scan-type full --delay 2.0
```

### Tip 2: Use request files for reproducibility
```bash
# Save your working configuration
--request-file tested_config.json
```

### Tip 3: Generate both report formats
```bash
python src/rag_scanner.py --url URL --format json
python src/rag_scanner.py --url URL --format html
```

### Tip 4: Use environment variables
```bash
# In .env file
TARGET_URL=https://api.example.com/chat
OPENAI_API_KEY=sk-xxx

# Then just run
python src/rag_scanner.py --scan-type full
```

### Tip 5: Test different HTTP methods
```bash
# Some APIs expose different vulnerabilities on GET vs POST
python src/rag_scanner.py --url URL --method POST --param prompt
python src/rag_scanner.py --url URL --method GET --param query
```

## 🎓 Learning Path

1. **Start**: Run demo mode
   ```bash
   python src/rag_scanner.py --demo
   ```

2. **Practice**: Test with different parameters
   ```bash
   python src/rag_scanner.py --demo --param custom_param
   ```

3. **Apply**: Test a real API
   ```bash
   python src/rag_scanner.py --url YOUR_API --scan-type prompt
   ```

4. **Master**: Use request files and full scans
   ```bash
   python src/rag_scanner.py --request-file config.json --scan-type full
   ```

## 📞 Getting Help

1. Check **USAGE_GUIDE.md** for detailed examples
2. Review **examples/** directory
3. Run with `--verbose` for debugging
4. Open GitHub issue if stuck

---

**Quick Start Command:**
```bash
python src/rag_scanner.py --demo --scan-type prompt
```

**Production Scan Command:**
```bash
python src/rag_scanner.py \
    --url YOUR_API_URL \
    --method POST \
    --param prompt \
    --scan-type full \
    --format html \
    --delay 2.0
```
