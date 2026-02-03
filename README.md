# CHATBOT (Streamlit)

Quick web-based chatbot using multiple LLM providers.

Setup

1. Create a virtual environment and install deps:

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\Activate.ps1 on Windows PowerShell
pip install -r CHATBOT/requirements.txt
```

2. Copy `.env.example` to `.env` and set your keys:

```bash
cp CHATBOT/.env.example CHATBOT/.env
# edit CHATBOT/.env to add keys
```

3. Run the app:

```bash
streamlit run CHATBOT/app.py
```

Providers supported in the dropdown:
- OpenAI (uses `OPENAI_API_KEY`)
- Gemini (generic HTTP endpoint; set `GEMINI_API_KEY` and `GEMINI_ENDPOINT`)
- Ollama - Mistral / Ollama - llama3 (local Ollama server; set `OLLAMA_URL` and optional `OLLAMA_MODEL`)

Notes
- The `CHATBOT/llm.py` file contains `init_model()` and `send_message()` helper functions. Adjust parsing to fit any specific provider API responses.
- Gemini support is left generic — adapt `GEMINI_ENDPOINT` and response parsing according to the API you intend to use.
