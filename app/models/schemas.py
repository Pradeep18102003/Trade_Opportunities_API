from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class AnalysisResponse(BaseModel):
    sector: str
    report_markdown: str