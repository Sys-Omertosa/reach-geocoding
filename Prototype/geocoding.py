# Module to perform geocoding
# getPlaceID(name: string) -> UUID


##############################################
import geopandas
from shapely.geometry import shape, MultiPolygon, Polygon
import requests
from dotenv import load_dotenv
import os

load_dotenv('../local.env', override=True)
LOCATION_IQ_KEY = os.getenv("LOCATION_IQ_KEY")

def getResponse(location: str):
    location = location.strip().lower()
    url = f"https://us1.locationiq.com/v1/search?q={location}&format=json&countrycodes=pk&key={LOCATION_IQ_KEY}"