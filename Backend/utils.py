import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from supabase import create_client, Client

# Load environment variables at module level using multiple fallback strategies
def _load_env():
    """
    Load environment variables using multiple fallback strategies to ensure
    the .env file is found regardless of where the script is executed from.
    """
    # Strategy 1: Use find_dotenv() which searches up the directory tree
    env_file = find_dotenv(filename='local.env', raise_error_if_not_found=False, usecwd=True)
    if env_file:
        load_dotenv(env_file, override=True)
        return True
    
    # Strategy 2: Look for .env file relative to this utils.py file
    utils_dir = Path(__file__).parent
    local_env_path = utils_dir / 'local.env'
    if local_env_path.exists():
        load_dotenv(local_env_path, override=True)
        return True
    
    # Strategy 3: Check common project root locations
    possible_roots = [
        utils_dir,  # Backend directory
        utils_dir.parent,  # Project root
        Path.cwd(),  # Current working directory
    ]
    
    for root in possible_roots:
        env_paths = [
            root / 'local.env',
            root / '.env',
            root / 'Backend' / 'local.env',
        ]
        
        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path, override=True)
                return True
    
    return False

# Load environment variables when the module is imported
_env_loaded = _load_env()

def supabase_client():
    if not _env_loaded:
        raise RuntimeError(
            "Could not find environment file (local.env). "
            "Please ensure it exists in the Backend directory or project root."
        )
    
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise ValueError(
            "Missing required environment variables: SUPABASE_URL and/or SUPABASE_SERVICE_KEY. "
            "Please check your local.env file."
        )
        
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    return supabase


def get_env_var(key: str, default=None, required=True):
    """
    Get an environment variable with optional default and required validation.
    
    Args:
        key: Environment variable name
        default: Default value if not found (only used if required=False)
        required: Whether the variable is required (raises ValueError if missing)
    
    Returns:
        The environment variable value
        
    Raises:
        ValueError: If required=True and the variable is not set
    """
    value = os.getenv(key, default)
    
    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")
    
    return value


def reload_env():
    global _env_loaded
    _env_loaded = _load_env()
    return _env_loaded


def is_env_loaded():
    return _env_loaded