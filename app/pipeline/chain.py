# chain.py
import asyncio  
from app.pipeline.aggregator import aggregate_pages
from app.pipeline.summarizer import summarize_long_text
from app.prompt_manager import PromptManager
from app.providers.router import chat
from app.storage.brief_store import save_brief
from app.providers.router import get_client



# --- Orchestrator ---
async def generate_brief(company: str, url: str, tone: str = "formal", model="gpt-4o-mini"):
    # Step 1: Fetch + aggregate pages
    aggregated = await aggregate_pages([url], model=model)

    # Step 2: Summarize if oversized
    if isinstance(aggregated, str) and len(aggregated) > 10000:
        context = summarize_long_text(aggregated, model=model)
    else:
        context = aggregated

    # Step 3: Render brief generator prompt
    pm = PromptManager()
    messages = pm.render("brief_generator", tone=tone, content=context)

    # Step 4: Generate brief
    brief_md = chat(messages, model=model)

    # Step 5: Save to SQLite
    save_brief(company, url, brief_md)

    return brief_md

# --- Streaming variant (for Gradio) ---
async def stream_brief(company: str, url: str, tone: str = "formal", model="gpt-4o-mini"):
    pm = PromptManager()
    aggregated = await aggregate_pages([url], model=model)
    context = summarize_long_text(aggregated, model=model) if len(aggregated) > 10000 else aggregated
    messages = pm.render("brief_generator", tone=tone, content=context)

    client = get_client()  # from router.py
    with client.chat.completions.stream(model=model, messages=messages) as stream:
        for event in stream:
            if event.type == "message.delta":
                yield event.delta



if __name__ == "__main__":
    asyncio.run(generate_brief("HuggingFace", "https://huggingface.co/docs"))
    asyncio.run(generate_brief("OpenAI", "https://openai.com/research"))
    print("Briefs stored in data/briefs.db")
 