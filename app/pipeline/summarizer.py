# summarizer.py
import tiktoken
from app.prompt_manager import PromptManager
from app.providers.router import chat

# --- Chunking ---
def chunk_text(text, max_tokens=1500, model="gpt-4o-mini"):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    chunks = [tokens[i:i+max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [enc.decode(chunk) for chunk in chunks]

# --- Map step: summarize each chunk ---
def map_summarize(chunks, model="gpt-4o-mini"):
    pm = PromptManager()
    summaries = []
    for chunk in chunks:
        messages = pm.render("chunk_summarizer", tone="formal", chunk=chunk)
        summary = chat(messages, model=model)
        summaries.append(summary)
    return summaries

# --- Reduce step: combine summaries ---
def reduce_summaries(summaries, model="gpt-4o-mini"):
    pm = PromptManager()
    combined = " ".join(summaries)
    messages = pm.render("brief_generator", tone="formal", content=combined)
    return chat(messages, model=model)

# --- Full pipeline ---
def summarize_long_text(text, model="gpt-4o-mini"):
    chunks = chunk_text(text, max_tokens=1500, model=model)
    summaries = map_summarize(chunks, model=model)
    final_brief = reduce_summaries(summaries, model=model)
    return final_brief

