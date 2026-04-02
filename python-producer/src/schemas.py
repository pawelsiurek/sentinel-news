from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone

class NewsAlert(BaseModel):
    """
    The strict contract representing an analyzed news event.
    Both Python and Java must agree on this exact structure.
    """
    
    headline: str       = Field(..., description="News headline")
    impact_score: float = Field(..., ge=0.0, le=1.0, description="Market impact score according to AI (0.0 to 1.0)")
    category: str       = Field(..., description="Category of the news (e.g. Tech / Sport / Finance / Politics / ...)")
    timestamp: str      = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "headline": "US Govt. urges Nvidia to entirely stop shipping GPUs to China",
                "impact_score": 0.85,
                "category": "Tech",
                "timestamp": "2026-04-02T20:30:00.000000+00:00"
            }
        }
    )