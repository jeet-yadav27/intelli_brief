import os
import openai
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

def get_client():
    # Explicitly pass API key from environment
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Retry decorator ---
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def chat(messages, model="gpt-4o-mini", stream=False):
    client = get_client()
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream
    )
    return resp.choices[0].message.content

# --- Health check ---
def health_check():
    try:
        answer = chat([{"role": "user", "content": "ping"}])
        return {"openai": "OK"}
    except Exception as e:
        return {"openai": f"FAIL: {e}"}

if __name__ == "__main__":
    prompt = [{"role": "user", "content": "Tell me a fun fact about space"}]
    print("\n--- OPENAI ---")
    print(chat(prompt, model="gpt-4o-mini"))
    print("\nHealth Check:", health_check())
