import os
import requests
import openai
from dotenv import load_dotenv
import google.generativeai as genai
import ollama

load_dotenv()

def init_model(provider_name: str):
    provider_name = provider_name.lower()
    cfg = {"provider": provider_name}
    if provider_name == "openai":
        openai_api_key = os.getenv("OPENAI_API_KEY")
        cfg.update({"api_key": openai_api_key, "model": os.getenv("OPENAI_MODEL", "gpt-4")})
    elif provider_name == "gemini":
        cfg.update({"api_key": os.getenv("GEMINI_API_KEY"), "model": os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")})
    elif provider_name.startswith("ollama"):
        cfg.update({"url": os.getenv("OLLAMA_URL", "http://localhost:11434")})
        if "mistral" in provider_name:
            cfg["model"] = "mistral"
        elif "llama3" in provider_name or "llama-3" in provider_name:
            cfg["model"] = "llama3"
        else:
            cfg["model"] = os.getenv("OLLAMA_MODEL", "mistral")
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
    return cfg


def send_message(cfg: dict, message: str, history: list = None) -> str:
    history = history or []
    print("History:", history)
    provider = cfg.get("provider")
    if provider == "openai":
        print(cfg)
        system = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")
        # Start with system prompt
        messages = [{"role": "system", "content": system}]
        # Add history if present
        if history:
            for turn in history:
                messages.append({"role": turn[0], "content": turn[1]})
        # Add current user message
        print(messages)
        # Support both new (openai>=1.0.0) and older openai-python SDKs
        from openai import OpenAI
        client = OpenAI(api_key=cfg.get("api_key"))
        resp = client.chat.completions.create(model=cfg.get("model"), messages=messages)
        return resp.choices[0].message.content.strip()  
    elif provider == "gemini":
        print(cfg)
        gemini_api_key = cfg.get("api_key")
        genai.configure(api_key=gemini_api_key)
        model_name = cfg.get("model")
        model = genai.GenerativeModel(model_name)
        system = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")
        # Format history as a conversation
        conversation = [f"System: {system}"]
        for turn in history:
           
            role = turn[0].capitalize()
            content = turn[1]
            conversation.append(f"{role}: {content}")
   
        #conversation.append(f"User: {message}")
        prompt = "\n".join(conversation)
        print("Prompt:", prompt)
        response = model.generate_content(prompt)
        return response.text.strip()
    elif provider.startswith("ollama"):
        print(cfg)
        system = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")
        # Start with system prompt
        messages = [{"role": "system", "content": system}]
        # Add history if present
        if history:
            for turn in history:
                messages.append({"role": turn[0], "content": turn[1]})
        print("Prompt:", messages)
        model = cfg.get("model")
        response = ollama.generate(model=model, prompt=message)
        return response['response'].strip()
    else:
        return "Provider not supported"
