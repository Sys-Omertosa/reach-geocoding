import os
import json
from openai import OpenAI
from utils import load_dotenv

configs = json.load("llm_configs.json")
load_dotenv()

# Unified LLM client with abstraction, based on Openai
class LLMClient:
    def __init__(self, model: str):
        if model not in configs:
            raise ValueError(f"Model not configured: {model}")
        
        self.model = model
        self.config = configs[model]
        self._client = self._create_client()

    def _create_client(self) -> OpenAI:
        # Create an OpenAI client with the configured key and base_url
        key = os.getenv(self.config.get("api_key_name"))
        url = self.config.get("base_url")

        return OpenAI(api_key=key, base_url=url)
    
    def call(self, messages, **kwargs):
        # Make a call to the LLM

        #Merge default and custom params
        params = {**self.config["default_params"], **kwargs}
        
        return self._client.chat.completions.create(
            model = self.model,
            messages=messages,
            **params
        )