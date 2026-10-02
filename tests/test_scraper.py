# test_scraper.py
import pytest
import asyncio
from app.scraper.advanced import fetch_smart

@pytest.mark.asyncio
async def test_fetch_smart_openai():
    text = await fetch_smart("https://openai.com")
    assert len(text) > 500
    assert "---SCRAPER OUTPUT START---" in text
    assert "---SCRAPER OUTPUT END---" in text
