from fastapi import Request
from fastapi.responses import JSONResponse

class ExternalAPIError(Exception):
    """Custom exception raised when an external API (DuckDuckGo or Gemini) fails."""
    def __init__(self, service_name: str, message: str):
        self.service_name = service_name
        self.message = message

async def external_api_exception_handler(request: Request, exc: ExternalAPIError):
    """Catches ExternalAPIErrors and formats them into a clean JSON response."""
    return JSONResponse(
        status_code=503,
        content={
            "error": "Service Unavailable",
            "detail": f"The {exc.service_name} integration failed. {exc.message}"
        },
    )