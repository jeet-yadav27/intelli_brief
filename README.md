# IntelliBrief

IntelliBrief is a FastAPI-powered application that scrapes, classifies, and summarizes web content into concise briefs.  
It supports conversational Q&A over stored briefs using LangChain orchestration and Groq LLMs.

---

## 🚀 Features
- **FastAPI backend** with CLI entry point
- **Scraper**: requests + BeautifulSoup, Playwright fallback
- **Pipeline**: link classification, async aggregation, summarization
- **Storage**: SQLite persistence + ChromaDB vector store
- **Chat**: conversational Q&A over briefs
- **UI**: Gradio front-end
- **Observability**: LLM call logging

---

## 📂 Project Structure
