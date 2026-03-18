import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.schemas import TokenResponse, AnalysisResponse
from app.core.security import create_access_token
from app.api.dependencies import limiter, get_current_user
from app.services.search_service import get_market_data
from app.services.llm_service import generate_report
from app.core.exceptions import ExternalAPIError

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/auth/guest", response_model=TokenResponse, tags=["Authentication"])
async def get_guest_token():
    """Generate a temporary guest token to test the API."""
    access_token = create_access_token(data={"sub": "guest_user"})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/analyze/{sector}", response_model=AnalysisResponse, tags=["Analysis"])
@limiter.limit("5/minute") # Rate limiting: 5 requests per minute per IP
async def analyze_sector(request: Request, sector: str, user: str = Depends(get_current_user)):
    """Analyze a sector and return a markdown report (Requires Bearer Token)."""
    
    # Input Validation
    if not sector.isalpha():
        raise HTTPException(status_code=400, detail="Sector must contain only letters.")

    try:
        # Step 1: Collect Data
        logger.info(f"Fetching data for sector: {sector}")
        context_data = await get_market_data(sector)
        
        # Step 2: Generate Report
        logger.info(f"Generating Gemini report for sector: {sector}")
        report_md = await generate_report(sector, context_data)
        
        # Step 3: Return Response
        return AnalysisResponse(sector=sector, report_markdown=report_md)
        
    except Exception as e:
        logger.error(f"Failed to process request: {str(e)}")
        raise ExternalAPIError(service_name="Analysis Pipeline", message="Please try again later.")