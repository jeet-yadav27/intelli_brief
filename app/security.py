# security.py
import re
from fastapi import HTTPException, Header

def validate_url(url: str) -> str:
    """
    Validate incoming URLs to prevent SSRF attacks.
    Blocks localhost, private IP ranges, and file:// schemes.
    """
    blocked_patterns = [
        r"^http://127\.", r"^http://0\.", r"^http://localhost",
        r"^http://10\.", r"^http://192\.168\.",
        r"^http://172\.(1[6-9]|2[0-9]|3[0-1])\.",
        r"^file://"
    ]
    for pattern in blocked_patterns:
        if re.match(pattern, url):
            raise HTTPException(status_code=400, detail="Invalid or unsafe URL")
    return url

def verify_api_key(x_api_key: str = Header(...)):
    """
    Require a valid API key in request headers.
    """
    if x_api_key != "expected_api_key":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key
