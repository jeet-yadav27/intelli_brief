# test_security.py
import pytest
from fastapi import HTTPException
from app.security import validate_url


malicious_urls = [
    "http://127.0.0.1",
    "http://localhost",
    "http://10.0.0.5",
    "http://192.168.1.1",
    "file:///etc/passwd"
]

def test_malicious_urls_blocked():
    for url in malicious_urls:
        with pytest.raises(HTTPException):
            validate_url(url)

def test_safe_url_passes():
    assert validate_url("http://example.com") == "http://example.com"
