import asyncio
import logging
from ddgs import DDGS

logger = logging.getLogger(__name__)

def _fetch_search_results(query: str) -> str:
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No recent data found."
        
        context = ""
        for res in results:
            context += f"Title: {res.get('title')}\nSnippet: {res.get('body')}\n\n"
        return context
    except Exception as e:
        logger.error(f"Search API error: {str(e)}")
        raise e

async def get_market_data(sector: str) -> str:
    query = f"{sector} sector market analysis trade opportunities India 2026 recent news"
    # Run synchronous DuckDuckGo search in an async executor
    return await asyncio.to_thread(_fetch_search_results, query)