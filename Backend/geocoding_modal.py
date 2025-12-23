"""
Geocoding Modal Endpoint

Modal.com deployment for the geocoding microservice.
Provides a web endpoint that accepts a list of place names and returns their IDs.

Usage:
    modal deploy geocoding_modal.py
    
    curl -X POST "https://[your-modal-url]/geocode" \
      --header "Authorization: Bearer YOUR_SECRET_KEY" \
      --header "Content-Type: application/json" \
      --data '{"place_names": ["Islamabad", "Lahore", "Karachi"]}'
"""

import modal
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List
import os

#################################################
# AUTH & MODELS
#################################################

auth_scheme = HTTPBearer()

class GeocodeRequest(BaseModel):
    """Request model for geocoding endpoint"""
    place_names: List[str] = Field(
        ..., 
        description="List of place names to geocode",
        example=["Islamabad", "Lahore", "Central Sindh"]
    )

class GeocodeResponse(BaseModel):
    """Response model for geocoding endpoint"""
    status: str = Field(
        description="Status of the request",
        example="success"
    )
    place_ids: List[str] = Field(
        description="List of place IDs corresponding to input names. Empty string if no match found.",
        example=["uuid-1", "uuid-2", "uuid-3"]
    )
    count: int = Field(
        description="Number of places processed",
        example=3
    )

#################################################
# IMAGE & APP SETUP
#################################################

image = (
    modal.Image.debian_slim()
    .pip_install(
        "fastapi",
        "uvicorn",
        "supabase",
        "python-dotenv",
        "pydantic",
        "pydantic-settings",
        "httpx",
        "rapidfuzz",
        "geopy",
        "redis"
    )
    .add_local_dir("geocoding", remote_path="/root/geocoding")
)

app = modal.App(name="reach-geocoder", image=image)

#################################################
# GEOCODING FUNCTION
#################################################

@app.function(
    secrets=[modal.Secret.from_name("reach-secrets")],
    timeout=300  # 5 minutes timeout
)
async def geocode_places(place_names: List[str]) -> List[str]:
    """
    Internal function that performs the actual geocoding.
    Uses the geocoding service to convert place names to IDs.
    
    Args:
        place_names: List of place name strings
        
    Returns:
        List of place ID strings (empty string if no match)
    """
    import logging
    from geocoding import get_geocoding_service
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Geocoding {len(place_names)} places")
        
        # Initialize the geocoding service
        service = get_geocoding_service()
        
        # Use the simple batch geocoding interface
        place_ids = await service.geocode_batch_simple(place_names)
        
        logger.info(f"Successfully geocoded {len([id for id in place_ids if id])} places")
        return place_ids
        
    except Exception as e:
        logger.error(f"Geocoding error: {e}", exc_info=True)
        # Return empty strings for all places on error
        return [""] * len(place_names)

#################################################
# WEB ENDPOINT (Authentication & Request Handling)
#################################################

@app.function(secrets=[modal.Secret.from_name("reach-secrets")])
@modal.fastapi_endpoint(method="POST")
async def geocode(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    request: GeocodeRequest = GeocodeRequest(place_names=[])
) -> GeocodeResponse:
    """
    FastAPI endpoint that authenticates requests and geocodes place names.
    
    Accepts a list of place name strings and returns their corresponding place IDs
    from the Pakistan administrative boundary hierarchy.
    
    Args:
        token: Bearer token for authentication
        request: GeocodeRequest containing list of place names
        
    Returns:
        GeocodeResponse with place IDs
        
    Raises:
        HTTPException: If authentication fails or request is invalid
    """
    # Validate authentication
    if token.credentials != os.environ.get("SECRET_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Validate request
    if not request.place_names:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="place_names list cannot be empty"
        )
    
    # Perform geocoding
    place_ids = await geocode_places.remote.aio(request.place_names)
    
    return GeocodeResponse(
        status="success",
        place_ids=place_ids,
        count=len(place_ids)
    )

#################################################
# HEALTH CHECK ENDPOINT
#################################################

@app.function()
@modal.fastapi_endpoint(method="GET")
async def health() -> dict:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "reach-geocoder",
        "version": "1.0.0"
    }
