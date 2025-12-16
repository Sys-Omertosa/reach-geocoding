import os
from openai import OpenAI
from pathlib import Path
from utils import load_env
import json

# Load env into the system
load_env()

# Load config file
CURRENT_DIR = Path(__file__).parent
config_path = CURRENT_DIR / "llm_configs.json"
with open(config_path, 'r') as f:
    configs = json.load(f)

# Unified LLM client with abstraction, based on Openai
class LLMClient:
    def __init__(self, model: str):
        if model not in configs:
            raise ValueError(f"Model not configured: {model}")
        
        self.model = model
        self.config = configs[model]
        self._client = self._create_client()

    def _create_client(self) -> OpenAI:
        """Create an OpenAI client with the configured key and base_url"""
        key = os.getenv(self.config.get("api_key_name"))
        if not key:
            raise ValueError(f"API key not found for {self.config.get('api_key_name')}")
        
        url = self.config.get("base_url")

        return OpenAI(api_key=key, base_url=url)
    
    def call(self, messages, **kwargs):
        """Make a call to the LLM"""
        #call(self, messages, **kwargs)
        #Merge default and custom params
        params = {**self.config["default_params"], **kwargs}
        #params = self.config["default_params"]
        
        response = self._client.chat.completions.create(
            model = self.config["model"],
            messages=messages,
            **params
        )
        return response.choices[0].message.content