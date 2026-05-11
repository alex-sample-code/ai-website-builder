"""
Analytics schemas
"""

from pydantic import Field
from datetime import date
from typing import Dict, Any
from app.schemas.common import BaseSchema


class AnalyticsOverviewRequest(BaseSchema):
    """Schema for analytics overview request"""

    start_date: date
    end_date: date


class AnalyticsOverviewResponse(BaseSchema):
    """Schema for analytics overview response"""

    total_pageviews: int
    total_unique_visitors: int
    trend_data: list[Dict[str, Any]]
    change_percentage: float | None = None


class PageRankingResponse(BaseSchema):
    """Schema for page ranking response"""

    page_path: str
    pageviews: int
    unique_visitors: int


class SourceAnalysisResponse(BaseSchema):
    """Schema for source analysis response"""

    referrer: str
    visits: int
    percentage: float


class DeviceBreakdownResponse(BaseSchema):
    """Schema for device breakdown response"""

    device_type: str
    count: int
    percentage: float


class AnalyticsTrackRequest(BaseSchema):
    """Schema for public analytics tracking beacon"""

    page_path: str = Field(..., min_length=1)
    referrer: str | None = None
    visitor_id: str | None = None
