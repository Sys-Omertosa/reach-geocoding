import os
from dotenv import load_dotenv
from pathlib import Path
from supabase import create_client, Client

def load_env():
    BASE_DIR = Path(__file__).resolve().parent
    ENV = BASE_DIR / 'local.env'
    load_dotenv(ENV, override=True)

_env_loaded = load_env()

def supabase_client():
    if not is_env_loaded():
        load_env()

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    return supabase

def reload_env():
    global _env_loaded
    _env_loaded = load_env()
    return _env_loaded

def is_env_loaded():
    return _env_loaded