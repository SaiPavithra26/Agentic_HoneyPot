import requests

class BedrockLLM:  # keep name so other imports don't change
    def __init__(self, model="llama3", base_url="http://localhost:11434"):
        self.model = model
        self.url = f"{base_url}/api/generate"

    def ask(self, prompt: str) -> str:
        resp = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        resp.raise_for_status()
        return resp.json()["response"].strip()
