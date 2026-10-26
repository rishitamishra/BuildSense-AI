from typing import List, Optional
from pydantic import BaseModel

class Finding(BaseModel):
    issue: str
    severity: str
    evidence: str
    recommended_action: str

class Safety(BaseModel):
    overall_risk: str
    findings: List[Finding] = []

class Cracks(BaseModel):
    observed: bool
    crack_type: str
    severity: str
    probable_causes: List[str] = []
    recommended_actions: List[str] = []
    disclaimer: str = "Preliminary image-only assessment; obtain a qualified on-site inspection."

class Material(BaseModel):
    item: str
    quantity: str
    estimated_cost_inr: float = 0

class Planning(BaseModel):
    project_summary: str
    estimated_duration_days: int = 0
    milestones: List[str] = []
    materials: List[Material] = []
    estimated_total_cost_inr: float = 0

class Valuation(BaseModel):
    estimated_value_inr: Optional[float] = None
    assumptions: List[str] = []
    confidence: str = "low"
    note: str = "Indicative only; local market data and professional valuation are required."

class SiteAdvice(BaseModel):
    advice: List[str] = []
    weather_note: str = "Live weather is not connected; check a local forecast."

class Analysis(BaseModel):
    mode: str
    summary: str
    safety: Safety
    cracks: Cracks
    planning: Planning
    valuation: Valuation
    site_advice: SiteAdvice
    limitations: List[str] = []
