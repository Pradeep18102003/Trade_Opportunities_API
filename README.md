# 📈 Trade Opportunities API

An automated AI research assistant built with **FastAPI**. This application dynamically scrapes the web for the latest market news in a specified Indian sector, and uses the **Google Gemini 1.5 Flash** model to generate a structured Markdown report highlighting key trade opportunities, market drivers, and potential risks.

Built as a lightweight, in-memory, zero-database application prioritizing **speed, security, and separation of concerns.**

## ✨ Features

* **Real-time Data Scraping:** Uses DuckDuckGo Search to fetch the most recent news and market analysis without requiring paid search APIs.
* **AI-Powered Analysis:** Integrates Google's Gemini LLM to synthesize raw web data into clean, structured Markdown reports.
* **JWT Authentication:** Includes a guest authentication endpoint to secure the analysis pipeline.
* **Rate Limiting:** Protects the external APIs (and your wallet) using `slowapi`, strictly limiting users to 5 requests per minute per IP.
* **Graceful Error Handling:** Custom exception handlers ensure the API never crashes ungracefully, returning clean `503 Service Unavailable` JSON responses if upstream APIs fail.
* **Comprehensive Testing:** Includes a suite of automated unit tests using `pytest` and `unittest.mock` to ensure reliability without hitting live API endpoints.

## 🏗️ Architecture & Project Structure

This project follows a **Domain-Driven Design (DDD)** inspired layered architecture. By strictly separating routing, business logic, and configuration, the codebase remains highly maintainable and testable.

```text
Trade_Opportunities_API/
├── app/
│   ├── main.py                 # FastAPI application instance and middleware setup
│   ├── api/                    # Routing Layer (Controllers & Dependencies)
│   ├── core/                   # Application-wide settings & Exception handlers
│   ├── models/                 # Pydantic Schemas for Input/Output validation
│   └── services/               # Business Logic Layer (Search & LLM integration)
├── tests/                      # Pytest suite with mocked external APIs
├── .env.example                # Template for environment variables
└── requirements.txt            # Project dependencies
```
## 🚀 Getting Started
Follow these instructions to get the project up and running on your local machine.

### Prerequisites
- Python 3.9 or higher

- A Google Gemini API Key

1. Clone the repository
```bash
git clone https://github.com/Pradeep18102003/Trade_Opportunities_API.git
cd Trade_Opportunities_API
```
2. Set up the virtual environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Configure Environment Variables
Create a file named .env in the root directory.

```bash
# .env
GEMINI_API_KEY=your_actual_gemini_api_key_here
SECRET_KEY=any_random_secure_string_here
```
5. Run the Server
```bash
uvicorn app.main:app --reload
```
The API will start at http://127.0.0.1:8000.

## 📖 API Usage (How to test)

You can test this API in two ways: using the interactive browser interface, or using the included Python command-line client. 

**Note:** Ensure the FastAPI server is running first (`uvicorn app.main:app --reload`).

### Method 1: Using the Python CLI Client (Recommended)
We have included a simple Python script that acts as a client. It automatically handles authentication, fetches the AI analysis, and saves the output as a clean `.md` file on your computer.

1. Open a **new** terminal window (keep the server running in the first one).
2. Ensure your virtual environment is activated.
3. Run the client script:
   ```bash
   python run_client.py
   ```
4. Enter a sector when prompted (e.g., healthcare, renewable energy).

5. The script will fetch the data and save a file like <sector_name>_market_report.md directly in your project folder!

### Method 2: Using the Interactive Browser Interface (Swagger UI)
FastAPI provides a built-in UI to test endpoints manually.

- Open your browser and navigate to https://www.google.com/search?q=http://127.0.0.1:8000/docs.

Authenticate:

- Expand POST /auth/guest and click Try it out -> Execute.

- Scroll down to the response and copy the access_token string (without quotes).

- Scroll to the top of the page, click the green Authorize button, paste the token into the Value box, and click Authorize.

Analyze:

- Expand GET /analyze/{sector}.

- Click Try it out and enter a sector (e.g., technology).

- Click Execute to see the AI-generated Markdown report in the response body!
## 🧪 Running Tests
To run the automated test suite (which mocks the LLM and Web Search to run instantly without using quota):

```Bash
pytest
```



