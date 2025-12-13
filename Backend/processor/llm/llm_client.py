import os
from openai import OpenAI
from utils import load_env

load_env()
configs = {
    "ernie-4.5-vl": {
        "model": "ernie-4.5-vl-28b-a3b-thinking",
        "api_key_name": "BAIDU_KEY",
        "base_url": "https://aistudio.baidu.com/llm/lmapi/v3",
        "default_params": {
            "extra_body": {
                "penalty_score": 1
            },
            "max_completion_tokens": 128000,
            "temperature": 0.6,
            "top_p": 0.95,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
    },
    "ernie-x1": {
        "model": "ernie-x1.1-preview",
        "api_key_name": "BAIDU_KEY",
        "base_url": "https://aistudio.baidu.com/llm/lmapi/v3",
        "default_params": {
            "web_search": {
                "enable": "True"
            },
            "max_completion_tokens": 65536,
            "response_format": {
                "type": "json_object"
            }
        }
    }
}

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