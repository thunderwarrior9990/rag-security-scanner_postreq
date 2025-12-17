# RAG Security Scanner - Example Workflows

## 🎯 Real-World Testing Scenarios

### Scenario 1: Testing a New AI Chatbot

**Situation**: You built a chatbot and want to test for security vulnerabilities.

**Workflow**:

```bash
# Step 1: Quick test to see if it works
python src/rag_scanner.py --url https://your-chatbot.com/api/chat --demo --scan-type prompt

# Step 2: Find the correct parameter name
# Try different common parameter names
python src/rag_scanner.py --url https://your-chatbot.com/api/chat --param message --demo
python src/rag_scanner.py --url https://your-chatbot.com/api/chat --param prompt --demo
python src/rag_scanner.py --url https://your-chatbot.com/api/chat --param user_input --demo

# Step 3: Full security scan with correct parameter
python src/rag_scanner.py \
    --url https://your-chatbot.com/api/chat \
    --method POST \
    --param user_input \
    --body-param session_id=test \
    --scan-type full \
    --format html \
    --delay 1.5
```

**Result**: Comprehensive HTML report showing all vulnerabilities

---

### Scenario 2: Testing Multiple AI Services

**Situation**: Your company uses multiple AI APIs, and you need to audit all of them.

**Workflow**:

**Step 1**: Create configuration file `company_ai_services.json`:
```json
[
  {
    "method": "POST",
    "url": "https://chatbot.company.com/api/chat",
    "param_name": "message",
    "additional_params": {
      "model": "gpt-4",
      "session_id": "audit-test"
    }
  },
  {
    "method": "POST",
    "url": "https://summarizer.company.com/api/summarize",
    "param_name": "text",
    "additional_params": {
      "max_length": 200
    }
  },
  {
    "method": "GET",
    "url": "https://search.company.com/api/query",
    "param_name": "q",
    "additional_params": {
      "limit": 10
    }
  },
  {
    "method": "POST",
    "url": "https://qa.company.com/api/ask",
    "param_name": "question",
    "additional_params": {
      "use_rag": true
    }
  }
]
```

**Step 2**: Run comprehensive audit:
```bash
python src/rag_scanner.py \
    --request-file company_ai_services.json \
    --scan-type full \
    --format html \
    --output company_security_audit_$(date +%Y%m%d).html \
    --delay 2.0
```

**Result**: Single report covering all 4 services

---

### Scenario 3: Testing OpenAI Integration

**Situation**: You're integrating OpenAI API and want to ensure it's secure.

**Workflow**:

```bash
# Set API key as environment variable (secure)
export OPENAI_API_KEY="sk-your-key-here"

# Run comprehensive scan
python src/rag_scanner.py \
    --url https://api.openai.com/v1/chat/completions \
    --api-format openai \
    --body-param model=gpt-3.5-turbo \
    --body-param max_tokens=150 \
    --scan-type full \
    --format html \
    --delay 2.0
```

**Result**: Security assessment of your OpenAI integration

---

### Scenario 4: Testing Custom RAG System

**Situation**: You built a custom RAG system and need to test for data leakage.

**Workflow**:

```bash
# Test data leakage specifically
python src/rag_scanner.py \
    --url https://my-rag-system.com/api/query \
    --method POST \
    --param question \
    --body-param use_vector_db=true \
    --body-param max_results=5 \
    --body-param context_enabled=true \
    --header "X-RAG-Version=1.0" \
    --scan-type data \
    --format html \
    --delay 1.0

# Then test prompt injection
python src/rag_scanner.py \
    --url https://my-rag-system.com/api/query \
    --method POST \
    --param question \
    --body-param use_vector_db=true \
    --scan-type prompt \
    --format html
```

**Result**: Focused reports on data leakage and prompt injection

---

### Scenario 5: Testing HuggingFace Model

**Situation**: You're using a HuggingFace hosted model and want to test it.

**Workflow**:

```bash
python src/rag_scanner.py \
    --url https://api-inference.huggingface.co/models/gpt2 \
    --method POST \
    --param inputs \
    --header "Authorization=Bearer hf_YOUR_TOKEN" \
    --body-param parameters.max_length=100 \
    --body-param parameters.temperature=0.7 \
    --scan-type full \
    --delay 3.0 \
    --timeout 60
```

**Result**: Security assessment respecting HuggingFace rate limits

---

### Scenario 6: Testing Search/Retrieval API

**Situation**: You have a search API that uses GET requests.

**Workflow**:

```bash
python src/rag_scanner.py \
    --url https://search-api.example.com/search \
    --method GET \
    --param query \
    --body-param limit=10 \
    --body-param sort=relevance \
    --body-param format=json \
    --scan-type data \
    --format html
```

**Result**: Assessment of search API security

---

### Scenario 7: Testing with Different Parameter Locations

**Situation**: Your API accepts the user input in different nested locations.

**Workflow**:

**Test 1**: Top-level parameter
```bash
python src/rag_scanner.py \
    --url https://api.example.com/chat \
    --param prompt \
    --scan-type prompt
```

**Test 2**: Nested in messages array
```bash
python src/rag_scanner.py \
    --url https://api.example.com/chat \
    --param messages.0.content \
    --scan-type prompt
```

**Test 3**: Nested in query object
```bash
python src/rag_scanner.py \
    --url https://api.example.com/chat \
    --param query.text \
    --scan-type prompt
```

**Result**: Identify which parameter location is vulnerable

---

### Scenario 8: CI/CD Integration

**Situation**: You want to run security tests in your CI/CD pipeline.

**Workflow**:

**Step 1**: Create `ci_security_config.json`:
```json
[
  {
    "method": "POST",
    "url": "https://staging-api.example.com/chat",
    "param_name": "prompt",
    "additional_params": {"model": "gpt-4"}
  }
]
```

**Step 2**: Add to CI pipeline (e.g., GitHub Actions):
```yaml
# .github/workflows/security-scan.yml
name: AI Security Scan
on: [push, pull_request]
jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Security Scanner
        run: |
          python src/rag_scanner.py \
            --request-file ci_security_config.json \
            --scan-type full \
            --format json \
            --output security-report.json
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: security-report
          path: security-report.json
```

**Result**: Automated security testing on every commit

---

### Scenario 9: Penetration Testing Report

**Situation**: You're a security consultant hired to audit an AI system.

**Workflow**:

**Step 1**: Reconnaissance - Try different configurations
```bash
# Try POST
python src/rag_scanner.py --url TARGET --method POST --param prompt --demo

# Try GET
python src/rag_scanner.py --url TARGET --method GET --param query --demo

# Try different parameter names
python src/rag_scanner.py --url TARGET --param message --demo
python src/rag_scanner.py --url TARGET --param user_input --demo
python src/rag_scanner.py --url TARGET --param text --demo
```

**Step 2**: Comprehensive testing
```bash
python src/rag_scanner.py \
    --url TARGET_URL \
    --method POST \
    --param IDENTIFIED_PARAM \
    --scan-type full \
    --format html \
    --output pentest_report_$(date +%Y%m%d).html \
    --delay 2.0
```

**Step 3**: Generate detailed report
```bash
python src/rag_scanner.py \
    --url TARGET_URL \
    --method POST \
    --param IDENTIFIED_PARAM \
    --scan-type full \
    --format json \
    --output pentest_data_$(date +%Y%m%d).json
```

**Result**: Professional penetration testing report

---

### Scenario 10: Development Team Training

**Situation**: You want to train your dev team on AI security.

**Workflow**:

**Step 1**: Demo mode introduction
```bash
python src/rag_scanner.py --demo
```

**Step 2**: Show different attack types
```bash
# Prompt injection
python src/rag_scanner.py --demo --scan-type prompt

# Data leakage
python src/rag_scanner.py --demo --scan-type data

# Function abuse
python src/rag_scanner.py --demo --scan-type function
```

**Step 3**: Test their own APIs
```bash
python src/rag_scanner.py \
    --url THEIR_API_URL \
    --method POST \
    --param prompt \
    --scan-type full
```

**Result**: Educated team aware of AI security issues

---

## 📊 Common Patterns

### Pattern 1: Quick Assessment
```bash
python src/rag_scanner.py --url URL --demo --scan-type prompt
```

### Pattern 2: Full Audit
```bash
python src/rag_scanner.py \
    --url URL \
    --api-key KEY \
    --scan-type full \
    --format html \
    --delay 2.0
```

### Pattern 3: Multiple Endpoints
```bash
python src/rag_scanner.py --request-file endpoints.json --scan-type full
```

### Pattern 4: Targeted Testing
```bash
python src/rag_scanner.py --url URL --scan-type data  # Just data leakage
python src/rag_scanner.py --url URL --scan-type prompt  # Just prompt injection
```

### Pattern 5: Production-Safe Testing
```bash
python src/rag_scanner.py \
    --url URL \
    --scan-type prompt \
    --delay 5.0 \
    --timeout 120
```

---

## 🎯 Decision Tree: Which Command to Use?

```
Do you have multiple endpoints to test?
├─ YES → Use --request-file with JSON config
└─ NO ↓

Is it a GET or POST endpoint?
├─ GET → Use --method GET --param query
└─ POST → Use --method POST --param prompt

Do you need to add extra parameters?
├─ YES → Add --body-param key=value (multiple times)
└─ NO ↓

Do you need custom headers?
├─ YES → Add --header "Key=Value" (multiple times)
└─ NO ↓

What type of security test?
├─ Full audit → --scan-type full
├─ Prompt injection only → --scan-type prompt
├─ Data leakage only → --scan-type data
├─ Function abuse only → --scan-type function
└─ Context manipulation only → --scan-type context

What output format?
├─ HTML (visual report) → --format html
└─ JSON (data/CI) → --format json

Are you rate-limited?
├─ YES → Add --delay 3.0 --timeout 120
└─ NO → Use defaults
```

---

## 🚀 Complete Example: End-to-End Audit

**Scenario**: Full security audit of a production AI chatbot

```bash
#!/bin/bash
# complete_audit.sh - Full AI Security Audit Script

echo "🔍 Starting AI Security Audit..."

# 1. Quick reconnaissance
echo "Step 1: Reconnaissance..."
python src/rag_scanner.py \
    --url https://prod-chatbot.example.com/api/chat \
    --demo \
    --scan-type prompt \
    --delay 0.5

# 2. Test prompt injection
echo "Step 2: Testing Prompt Injection..."
python src/rag_scanner.py \
    --url https://prod-chatbot.example.com/api/chat \
    --method POST \
    --param user_message \
    --body-param session_id=audit-001 \
    --scan-type prompt \
    --format html \
    --output audit_prompt_injection.html \
    --delay 2.0

# 3. Test data leakage
echo "Step 3: Testing Data Leakage..."
python src/rag_scanner.py \
    --url https://prod-chatbot.example.com/api/chat \
    --method POST \
    --param user_message \
    --body-param session_id=audit-002 \
    --scan-type data \
    --format html \
    --output audit_data_leakage.html \
    --delay 2.0

# 4. Test function abuse
echo "Step 4: Testing Function Abuse..."
python src/rag_scanner.py \
    --url https://prod-chatbot.example.com/api/chat \
    --method POST \
    --param user_message \
    --body-param session_id=audit-003 \
    --scan-type function \
    --format html \
    --output audit_function_abuse.html \
    --delay 2.0

# 5. Full comprehensive scan
echo "Step 5: Full Comprehensive Scan..."
python src/rag_scanner.py \
    --url https://prod-chatbot.example.com/api/chat \
    --method POST \
    --param user_message \
    --body-param session_id=audit-004 \
    --scan-type full \
    --format html \
    --output audit_full_report.html \
    --format json \
    --output audit_full_data.json \
    --delay 2.0

echo "✅ Audit complete! Check the generated reports."
```

---

## 💡 Pro Tips

1. **Always start with demo mode** to understand output format
2. **Use request files** for reproducible testing
3. **Increase delays** for production environments
4. **Generate both HTML and JSON** reports
5. **Test incrementally** - start with one scan type
6. **Document your findings** in the reports
7. **Use environment variables** for API keys
8. **Version control** your request config files
9. **Automate testing** in CI/CD pipelines
10. **Share reports** with your security team

---

## 📞 Need Help?

- **Quick Start**: `python src/rag_scanner.py --demo`
- **Detailed Guide**: See `USAGE_GUIDE.md`
- **Quick Reference**: See `QUICK_REFERENCE.md`
- **Examples**: Check `examples/` directory
- **Tests**: Run `python3 test_enhancements.py`

---

**Remember**: Always get permission before testing production systems!
