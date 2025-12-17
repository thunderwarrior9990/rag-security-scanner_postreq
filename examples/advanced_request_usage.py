#!/usr/bin/env python3
"""
Advanced RAG Security Scanner Usage Examples
Demonstrates POST/GET requests with custom parameters
"""

from src.rag_scanner import RAGSecurityScanner, RequestConfig

def example_custom_post_request():
    """Example: Custom POST request with specific parameter"""
    print("=" * 60)
    print("Example 1: Custom POST Request")
    print("=" * 60)
    
    # Create custom request configuration
    config = RequestConfig(
        method="POST",
        param_name="user_input",  # Payload goes into 'user_input' parameter
        url="https://api.example.com/ai/chat",
        headers={
            "Content-Type": "application/json",
            "X-API-Version": "2.0"
        },
        additional_params={
            "session_id": "test-123",
            "model": "custom-gpt",
            "temperature": 0.7
        },
        api_format="generic"
    )
    
    scanner = RAGSecurityScanner(
        request_config=config,
        api_key="your-api-key",
        delay_between_requests=1.0
    )
    
    # Run specific scan
    threats = scanner.scan_prompt_injection()
    print(f"Found {len(threats)} threats")


def example_get_request():
    """Example: GET request with query parameter"""
    print("\n" + "=" * 60)
    print("Example 2: GET Request with Query Parameter")
    print("=" * 60)
    
    config = RequestConfig(
        method="GET",
        param_name="query",  # Payload goes into 'query' parameter
        url="https://api.example.com/search",
        additional_params={
            "limit": 10,
            "format": "json",
            "lang": "en"
        },
        api_format="generic"
    )
    
    scanner = RAGSecurityScanner(
        request_config=config,
        delay_between_requests=0.5
    )
    
    # Run data leakage scan
    threats = scanner.scan_data_leakage()
    print(f"Found {len(threats)} potential data leakage issues")


def example_openai_format():
    """Example: OpenAI API format"""
    print("\n" + "=" * 60)
    print("Example 3: OpenAI API Format")
    print("=" * 60)
    
    config = RequestConfig(
        method="POST",
        param_name="prompt",
        url="https://api.openai.com/v1/chat/completions",
        api_format="openai",
        additional_params={
            "model": "gpt-3.5-turbo",
            "max_tokens": 150,
            "temperature": 0.7
        }
    )
    
    scanner = RAGSecurityScanner(
        request_config=config,
        api_key="sk-your-openai-key",
        delay_between_requests=2.0
    )
    
    # Full security scan
    result = scanner.run_full_scan()
    scanner.save_report(result, "html")


def example_nested_parameter():
    """Example: Nested parameter using dot notation"""
    print("\n" + "=" * 60)
    print("Example 4: Nested Parameter Path")
    print("=" * 60)
    
    config = RequestConfig(
        method="POST",
        param_name="messages.0.content",  # Nested path for payload
        url="https://api.example.com/chat",
        body_template={
            "model": "gpt-4",
            "messages": [
                {
                    "role": "user",
                    "content": "PLACEHOLDER"
                }
            ],
            "max_tokens": 200
        },
        api_format="custom"
    )
    
    scanner = RAGSecurityScanner(
        request_config=config,
        api_key="your-key"
    )
    
    result = scanner.run_full_scan()
    print(f"Scan complete. Found {len(result.threats_found)} threats")


def example_multiple_endpoints_from_file():
    """Example: Load multiple requests from file"""
    print("\n" + "=" * 60)
    print("Example 5: Multiple Endpoints from File")
    print("=" * 60)
    
    # Scanner will load all configurations from the JSON file
    scanner = RAGSecurityScanner(
        request_file="examples/requests_json.json",
        api_key="your-api-key",
        delay_between_requests=1.5
    )
    
    # Run full scan across all endpoints
    result = scanner.run_full_scan()
    scanner.save_report(result, "json")
    scanner.save_report(result, "html")


def example_custom_ai_api():
    """Example: Custom AI API with specific format"""
    print("\n" + "=" * 60)
    print("Example 6: Custom AI API")
    print("=" * 60)
    
    config = RequestConfig(
        method="POST",
        param_name="question",
        url="https://my-rag-system.example.com/ask",
        headers={
            "Content-Type": "application/json",
            "X-RAG-Version": "1.0"
        },
        body_template={
            "question": "PAYLOAD_PLACEHOLDER",
            "context": {
                "use_vector_db": True,
                "max_results": 5
            },
            "options": {
                "temperature": 0.5,
                "streaming": False
            }
        },
        api_format="custom"
    )
    
    scanner = RAGSecurityScanner(
        request_config=config,
        api_key="custom-api-key"
    )
    
    # Test specific vulnerability
    threats = scanner.scan_function_abuse()
    print(f"Found {len(threats)} function abuse threats")


def example_huggingface_inference():
    """Example: HuggingFace Inference API"""
    print("\n" + "=" * 60)
    print("Example 7: HuggingFace Inference API")
    print("=" * 60)
    
    config = RequestConfig(
        method="POST",
        param_name="inputs",
        url="https://api-inference.huggingface.co/models/gpt2",
        headers={
            "Authorization": "Bearer hf_YOUR_TOKEN",
            "Content-Type": "application/json"
        },
        additional_params={
            "parameters": {
                "max_length": 100,
                "temperature": 0.7
            }
        },
        api_format="generic"
    )
    
    scanner = RAGSecurityScanner(
        request_config=config,
        delay_between_requests=3.0  # HuggingFace has rate limits
    )
    
    result = scanner.run_full_scan()
    print(f"Scan ID: {result.scan_id}")


if __name__ == "__main__":
    print("\nRAG Security Scanner - Advanced Examples")
    print("=" * 60)
    print("\nThese examples demonstrate various request configurations.")
    print("Uncomment the examples you want to run:\n")
    
    # Uncomment to run specific examples:
    # example_custom_post_request()
    # example_get_request()
    # example_openai_format()
    # example_nested_parameter()
    # example_multiple_endpoints_from_file()
    # example_custom_ai_api()
    # example_huggingface_inference()
    
    print("\nTo run real scans, uncomment the examples above")
    print("and update the URLs and API keys.")
