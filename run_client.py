import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def main():
    # 1. Ask the user for input
    print("=== Trade Opportunities API Client ===")
    sector = input("Enter the sector you want to analyze (e.g., healthcare, renewable energy): ").strip()
    
    if not sector:
        print("Sector cannot be empty. Exiting.")
        return

    print("\n1. Getting guest token...")
    try:
        auth_res = requests.post(f"{BASE_URL}/auth/guest")
        auth_res.raise_for_status() # Check for server connection errors
    except requests.exceptions.RequestException:
        print("❌ Failed to connect. Is your FastAPI server (uvicorn) running?")
        sys.exit(1)
    
    token = auth_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    print(f"2. Requesting analysis for '{sector}' (this takes a few seconds)...")
    analyze_res = requests.get(f"{BASE_URL}/analyze/{sector}", headers=headers)
    
    if analyze_res.status_code == 200:
        data = analyze_res.json()
        markdown_content = data["report_markdown"]
        
        # Clean the sector name so it makes a valid file name (e.g., "Renewable Energy" -> "renewable_energy")
        safe_sector_name = sector.replace(" ", "_").lower()
        filename = f"{safe_sector_name}_market_report.md"
        
        # Save the file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        print(f"✅ Success! Report saved cleanly to: {filename}")
    else:
        print(f"❌ API Error: {analyze_res.status_code} - {analyze_res.text}")

if __name__ == "__main__":
    main()