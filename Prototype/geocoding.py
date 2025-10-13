import geopandas
from shapely.geometry import shape, MultiPolygon, Polygon
import requests
from dotenv import load_dotenv
import os
from pathlib import Path

###########################################################################################

script_dir = Path(__file__).parent
env_path = script_dir.parent / 'local.env'

load_dotenv(env_path, override=True)
LOCATION_IQ_KEY = os.environ.get("LOCATION_IQ_KEY")

###########################################################################################

def getResponse(location: str) -> list:
    location = location.strip().lower()
    url = f"https://us1.locationiq.com/v1/search?q={location}&format=json&countrycodes=pk&normalizeaddress=1&normalizecity=1&polygon_geojson=1&key={LOCATION_IQ_KEY}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()