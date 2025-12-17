#!/usr/bin/env python3
"""
Test script for enhanced RAG Security Scanner features
Tests POST/GET requests, parameter specification, and request file parsing
"""

import os
import sys
import json
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_scanner import RAGSecurityScanner, RequestConfig, RequestFileParser


def test_request_config_creation():
    """Test 1: RequestConfig creation"""
    print("=" * 60)
    print("Test 1: RequestConfig Creation")
    print("=" * 60)
    
    config = RequestConfig(
        method="POST",
        param_name="user_input",
        url="https://api.example.com/chat",
        additional_params={"model": "gpt-4", "temperature": 0.7}
    )
    
    assert config.method == "POST"
    assert config.param_name == "user_input"
    assert config.url == "https://api.example.com/chat"
    assert config.additional_params["model"] == "gpt-4"
    
    print("✓ RequestConfig created successfully")
    print(f"  Method: {config.method}")
    print(f"  Param: {config.param_name}")
    print(f"  URL: {config.url}")
    print()


def test_simple_url_file_parsing():
    """Test 2: Parse simple URL list file"""
    print("=" * 60)
    print("Test 2: Simple URL File Parsing")
    print("=" * 60)
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("# Test URLs\n")
        f.write("POST https://api.example.com/chat\n")
        f.write("GET https://api.example.com/search\n")
        f.write("https://api.openai.com/v1/chat/completions\n")
        temp_file = f.name
    
    try:
        configs = RequestFileParser.parse_request_file(temp_file)
        
        assert len(configs) == 3
        assert configs[0].method == "POST"
        assert configs[0].url == "https://api.example.com/chat"
        assert configs[1].method == "GET"
        assert configs[1].url == "https://api.example.com/search"
        assert configs[2].method == "POST"  # Default
        
        print("✓ Parsed 3 URLs successfully")
        for i, cfg in enumerate(configs, 1):
            print(f"  {i}. {cfg.method} {cfg.url}")
        print()
    finally:
        os.unlink(temp_file)


def test_json_file_parsing():
    """Test 3: Parse JSON configuration file"""
    print("=" * 60)
    print("Test 3: JSON Configuration File Parsing")
    print("=" * 60)
    
    json_data = [
        {
            "method": "POST",
            "url": "https://api.example.com/chat",
            "param_name": "message",
            "api_format": "generic",
            "additional_params": {"model": "gpt-4"}
        },
        {
            "method": "GET",
            "url": "https://api.example.com/search",
            "param_name": "query",
            "additional_params": {"limit": 10}
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(json_data, f)
        temp_file = f.name
    
    try:
        configs = RequestFileParser.parse_request_file(temp_file)
        
        assert len(configs) == 2
        assert configs[0].method == "POST"
        assert configs[0].param_name == "message"
        assert configs[0].additional_params["model"] == "gpt-4"
        assert configs[1].method == "GET"
        assert configs[1].param_name == "query"
        
        print("✓ Parsed JSON config successfully")
        for i, cfg in enumerate(configs, 1):
            print(f"  {i}. {cfg.method} {cfg.url} (param: {cfg.param_name})")
        print()
    finally:
        os.unlink(temp_file)


def test_http_format_parsing():
    """Test 4: Parse HTTP request format"""
    print("=" * 60)
    print("Test 4: HTTP Request Format Parsing")
    print("=" * 60)
    
    http_request = """POST https://api.example.com/chat HTTP/1.1
Content-Type: application/json
Authorization: Bearer test-token

{
  "prompt": "test",
  "model": "gpt-3.5-turbo"
}


GET https://api.example.com/search HTTP/1.1
Accept: application/json
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(http_request)
        temp_file = f.name
    
    try:
        configs = RequestFileParser.parse_request_file(temp_file)
        
        assert len(configs) == 2
        assert configs[0].method == "POST"
        assert configs[0].url == "https://api.example.com/chat"
        assert "Authorization" in configs[0].headers
        assert configs[1].method == "GET"
        
        print("✓ Parsed HTTP request format successfully")
        for i, cfg in enumerate(configs, 1):
            print(f"  {i}. {cfg.method} {cfg.url}")
            print(f"      Headers: {list(cfg.headers.keys())}")
        print()
    finally:
        os.unlink(temp_file)


def test_scanner_with_post_config():
    """Test 5: Scanner with POST configuration"""
    print("=" * 60)
    print("Test 5: Scanner with POST Configuration")
    print("=" * 60)
    
    config = RequestConfig(
        method="POST",
        param_name="user_query",
        api_format="generic",
        additional_params={"model": "gpt-4", "temperature": 0.7}
    )
    
    scanner = RAGSecurityScanner(
        request_config=config,
        delay_between_requests=0.1
    )
    
    assert scanner.request_configs[0].method == "POST"
    assert scanner.request_configs[0].param_name == "user_query"
    
    print("✓ Scanner initialized with POST config")
    print(f"  Method: {scanner.request_configs[0].method}")
    print(f"  Parameter: {scanner.request_configs[0].param_name}")
    print(f"  Additional params: {scanner.request_configs[0].additional_params}")
    print()


def test_scanner_with_get_config():
    """Test 6: Scanner with GET configuration"""
    print("=" * 60)
    print("Test 6: Scanner with GET Configuration")
    print("=" * 60)
    
    config = RequestConfig(
        method="GET",
        param_name="query",
        url="https://api.example.com/search",
        additional_params={"limit": 10, "format": "json"}
    )
    
    scanner = RAGSecurityScanner(
        target_url="https://api.example.com/search",
        request_config=config,
        delay_between_requests=0.1
    )
    
    assert scanner.request_configs[0].method == "GET"
    assert scanner.request_configs[0].param_name == "query"
    assert scanner.target_url == "https://api.example.com/search"
    
    print("✓ Scanner initialized with GET config")
    print(f"  Method: {scanner.request_configs[0].method}")
    print(f"  Parameter: {scanner.request_configs[0].param_name}")
    print(f"  URL: {scanner.target_url}")
    print()


def test_scanner_with_request_file():
    """Test 7: Scanner with request file"""
    print("=" * 60)
    print("Test 7: Scanner with Request File")
    print("=" * 60)
    
    json_data = [
        {
            "method": "POST",
            "url": "https://api1.example.com/chat",
            "param_name": "message",
            "additional_params": {"model": "gpt-4"}
        },
        {
            "method": "GET",
            "url": "https://api2.example.com/search",
            "param_name": "query"
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(json_data, f)
        temp_file = f.name
    
    try:
        scanner = RAGSecurityScanner(
            request_file=temp_file,
            delay_between_requests=0.1
        )
        
        assert len(scanner.request_configs) == 2
        assert scanner.request_configs[0].method == "POST"
        assert scanner.request_configs[1].method == "GET"
        
        print("✓ Scanner loaded multiple configs from file")
        for i, cfg in enumerate(scanner.request_configs, 1):
            print(f"  {i}. {cfg.method} {cfg.url} (param: {cfg.param_name})")
        print()
    finally:
        os.unlink(temp_file)


def test_demo_scan():
    """Test 8: Run a quick demo scan"""
    print("=" * 60)
    print("Test 8: Demo Scan with Custom Config")
    print("=" * 60)
    
    config = RequestConfig(
        method="POST",
        param_name="test_param",
        api_format="generic"
    )
    
    scanner = RAGSecurityScanner(
        request_config=config,
        delay_between_requests=0.05
    )
    
    # Run a small subset of tests
    print("Running prompt injection test (first 3 payloads)...")
    payloads = scanner.payloads["prompt_injection"][:3]
    threats_found = 0
    
    for payload in payloads:
        success, response, response_time = scanner._make_request(payload)
        if success:
            threat = scanner._analyze_response(payload, response, "prompt_injection")
            if threat:
                threats_found += 1
    
    print(f"✓ Demo scan completed")
    print(f"  Tests run: 3")
    print(f"  Threats found: {threats_found}")
    print(f"  Total requests: {scanner.total_requests}")
    print()


def test_nested_parameter_insertion():
    """Test 9: Nested parameter path"""
    print("=" * 60)
    print("Test 9: Nested Parameter Insertion")
    print("=" * 60)
    
    scanner = RAGSecurityScanner(delay_between_requests=0.1)
    
    # Test nested parameter insertion
    data = {}
    scanner._insert_payload_in_dict(data, "messages.0.content", "test payload")
    
    assert "messages" in data
    assert isinstance(data["messages"], list)
    assert data["messages"][0]["content"] == "test payload"
    
    print("✓ Nested parameter insertion works")
    print(f"  Result: {json.dumps(data, indent=2)}")
    print()


def run_all_tests():
    """Run all enhancement tests"""
    print("\n" + "=" * 60)
    print("RAG SECURITY SCANNER - ENHANCEMENT TESTS")
    print("=" * 60 + "\n")
    
    tests = [
        test_request_config_creation,
        test_simple_url_file_parsing,
        test_json_file_parsing,
        test_http_format_parsing,
        test_scanner_with_post_config,
        test_scanner_with_get_config,
        test_scanner_with_request_file,
        test_demo_scan,
        test_nested_parameter_insertion
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {str(e)}")
            print()
            failed += 1
    
    print("=" * 60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")
    
    if failed == 0:
        print("🎉 All tests passed! The enhancements are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
