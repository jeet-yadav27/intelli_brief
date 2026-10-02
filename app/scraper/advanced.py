import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from app.scraper.basic import fetch_with_requests

async def fetch_with_playwright(url: str) -> str:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=30000)
            content = await page.content()
            await browser.close()
            soup = BeautifulSoup(content, "html.parser")
            return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        print(f"[Playwright Error] {e}")
        return ""

async def fetch_smart(url: str) -> str:
    """
    Try requests first. If content < 500 chars, fallback to Playwright.
    Add delimiters to guard against prompt injection.
    """
    html = fetch_with_requests(url)
    if len(html) < 500:
        print("[Fallback Triggered] Switching to Playwright...")
        html = await fetch_with_playwright(url)

    if html:
        # Add delimiters for safety
        return f"\n---SCRAPER OUTPUT START---\n{html}\n---SCRAPER OUTPUT END---\n"
    return ""
