# aggregator.py
import asyncio
import httpx
import time
import logging
import tiktoken

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# --- Async fetcher ---
async def fetch_page(client, url):
    try:
        start = time.time()
        resp = await client.get(url, timeout=15)
        elapsed = round(time.time() - start, 2)
        logging.info(f"Fetched {url} in {elapsed}s, status={resp.status_code}")
        return {"url": url, "text": resp.text}
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return {"url": url, "text": ""}

async def fetch_all(urls):
    async with httpx.AsyncClient() as client:
        tasks = [fetch_page(client, u) for u in urls]
        return await asyncio.gather(*tasks)

# --- Token counter ---
def count_tokens(text, model="gpt-4o-mini"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

# --- Aggregator ---
async def aggregate_pages(urls, model="gpt-4o-mini"):
    pages = await fetch_all(urls)
    total_text = " ".join([p["text"] for p in pages if p["text"]])
    total_tokens = count_tokens(total_text, model=model)
    logging.info(f"Total tokens across {len(urls)} pages: {total_tokens}")

    if total_tokens > 6000:
        logging.info("Triggering map-reduce summarization...")
        # Here you would split into chunks and summarize each, then combine.
        return "Map-reduce summary triggered."
    else:
        logging.info("Content within token limit.")
        return total_text


