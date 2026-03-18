import logging
from google import genai  # <-- The new official Google library
from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialize the new Client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def generate_report(sector: str, context: str) -> str:
    prompt = f"""
    You are an expert Market Intelligence Analyst specializing in the Indian economy. 
    Generate a highly structured Markdown report focusing on trade opportunities in India's {sector} sector.
    
    Base your analysis STRICTLY on the following collected market data. Do not hallucinate.

    CONTEXT DATA:
    {context}

    OUTPUT FORMAT:
    Use the following Markdown structure exactly:

    # Market Analysis: Trade Opportunities in the Indian {sector.capitalize()} Sector

    ## Executive Summary
    [2-3 sentence overview based on the context]

    ## Key Trade Opportunities
    *   **[Opportunity 1]:** [Brief explanation based on data]
    *   **[Opportunity 2]:** [Brief explanation based on data]

    ## Market Drivers & Trends
    [Identify 2-3 current trends]

    ## Potential Risks or Barriers
    [Identify challenges mentioned in the context]
    """
    try:
        # The new syntax for asynchronous generation
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        raise e