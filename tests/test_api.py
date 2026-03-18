from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

# Create a test client that acts like a browser/frontend
client = TestClient(app)

def test_health_check():
    """Test that the API is up and running."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Trade Opportunities API is running."}

def test_guest_auth():
    """Test that the guest authentication endpoint returns a valid JWT token."""
    response = client.post("/auth/guest")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_analyze_unauthorized():
    """Test that the protected endpoint blocks requests without a token."""
    response = client.get("/analyze/technology")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

# The @patch decorators replace the real functions with fake (mocked) ones during the test
@patch("app.api.routes.generate_report", new_callable=AsyncMock)
@patch("app.api.routes.get_market_data", new_callable=AsyncMock)
def test_analyze_authorized_mocked(mock_get_data, mock_generate_report):
    """Test the complete workflow using mocked external APIs."""
    
    # 1. Setup the fake return values for our mocked functions
    mock_get_data.return_value = "Fake news about technology sector."
    mock_generate_report.return_value = "# Fake AI Markdown Report\n\n## Executive Summary\nTech is booming."

    # 2. Get a valid token
    auth_response = client.post("/auth/guest")
    token = auth_response.json()["access_token"]

    # 3. Make the request to the protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/analyze/technology", headers=headers)

    # 4. Assert the results are what we expect
    assert response.status_code == 200
    data = response.json()
    assert data["sector"] == "technology"
    assert "# Fake AI Markdown Report" in data["report_markdown"]
    
    # 5. Verify our mocked functions were actually called behind the scenes
    mock_get_data.assert_called_once_with("technology")
    mock_generate_report.assert_called_once()