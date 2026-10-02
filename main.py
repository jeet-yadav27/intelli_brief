# main.py
from fastapi import FastAPI
from app.config import settings
from fastapi import FastAPI, Depends
from app.security import validate_url, verify_api_key


app = FastAPI()

@app.get("/")
@app.get("/health")
def health_check():
    return {"status": "ok"}



@app.post("/api/v1/benchmark")
def benchmark(url: str, api_key: str = Depends(verify_api_key)):
    safe_url = validate_url(url)
    return {"message": f"Benchmarking {safe_url}"}
