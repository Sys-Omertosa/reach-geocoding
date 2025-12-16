from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

class QueueJob(BaseModel):    
    """Incoming job from Supabase queue"""
    document_id: str
    posted_date: datetime
    url: str
    title: str
    source: Literal["NDMA", "NEOC", "PMD"]
    filename: Optional[str]
    filetype: Literal["pdf", "pptx", "txt", "gif", "png", "jpeg"]
    raw_text: Optional[str] = None

class ExtractedContent(BaseModel):
    """Output from document processor"""
    job_id: str
    markdown: str
    extraction_method: Literal["vlm", "direct"]
    confidence_score: Optional[float] = None

# Alerts Enums
class AlertCategory(str, Enum):
    GEO = "Geo"
    MET = "Met"
    SAFETY = "Safety"
    SECURITY = "Security"
    RESCUE = "Rescue"
    FIRE = "Fire"
    HEALTH = "Health"
    ENV = "Env"
    TRANSPORT = "Transport"
    INFRA = "Infra"
    CBRNE = "CBRNE"
    OTHER = "Other"


class AlertUrgency(str, Enum):
    IMMEDIATE = "Immediate"
    EXPECTED = "Expected"
    FUTURE = "Future"
    PAST = "Past"
    UNKNOWN = "Unknown"


class AlertSeverity(str, Enum):
    EXTREME = "Extreme"
    SEVERE = "Severe"
    MODERATE = "Moderate"
    MINOR = "Minor"
    UNKNOWN = "Unknown"

#LLM Response
class Arealist(BaseModel):
    """Represents a specific area affected by the alert."""
    place_names: List[str]
    specific_effective_from: Optional[datetime] = None
    specific_effective_until: Optional[datetime] = None
    specific_urgency: Optional[AlertUrgency] = None
    specific_severity: Optional[AlertSeverity] = None
    specific_instruction: Optional[str] = None

class StructuredAlert(BaseModel):
    """Represents the response from the LLM, with unflattened area list"""
    category: AlertCategory
    event: str
    urgency: AlertUrgency
    severity: AlertSeverity
    description: str
    instruction: str
    effective_from: datetime
    effective_until: datetime
    areas: List[Arealist]

# For insertion into DB
class AlertArea(BaseModel):
    """Represents a specific area affected by the alert."""
    place_id: UUID
    specific_effective_from: Optional[datetime] = None
    specific_effective_until: Optional[datetime] = None
    specific_urgency: Optional[AlertUrgency] = None
    specific_severity: Optional[AlertSeverity] = None
    specific_instruction: Optional[str] = None

# Main alert data with areas
class AlertData(BaseModel):
    """Complete alert data that can be normalized into alerts and alert_areas tables."""
    document_id: UUID
    category: AlertCategory
    event: str
    urgency: AlertUrgency
    severity: AlertSeverity
    description: str
    instruction: str
    effective_from: datetime
    effective_until: datetime
    areas: List[AlertArea]
    alert_id: Optional[UUID] = None