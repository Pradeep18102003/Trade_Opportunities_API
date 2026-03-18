import logging
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api.routes import router
from app.api.dependencies import limiter
from app.core.exceptions import ExternalAPIError, external_api_exception_handler

# Configure simple logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Trade Opportunities API",
    description="Analyzes market data and provides trade opportunity insights for Indian sectors.",
    version="1.0.0"
)

# Add Rate Limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(ExternalAPIError, external_api_exception_handler)

# Include the API routes
app.include_router(router)

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Trade Opportunities API is running."}