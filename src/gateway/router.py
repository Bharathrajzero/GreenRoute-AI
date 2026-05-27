import os
import httpx

class LLMRouter:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "mock_key")
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    async def dispatch(self, prompt: str, target: str) -> str:
        if target == "Local-SLM":
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.ollama_host}/api/generate",
                        json={"model": "phi3", "prompt": prompt, "stream": False},
                        timeout=4.0
                    )
                    return response.json().get("response", "")
            except Exception:
                return f"[Mocked Free SLM Process] resolved locally on client architecture for: '{prompt}'"
        
        else:
            if self.openai_api_key == "mock_key":
                return f"[Mocked Cloud LLM Process] heavy reasoning analysis compiled for: '{prompt}'"
            
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=self.openai_api_key)
                completion = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                return completion.choices.message.content or ""
            except Exception as e:
                return f"Cloud layer failed: {str(e)}"
