import requests
import json
from pathlib import Path
from datetime import datetime
from config import FMP_API_KEY, BASE_URL
from logger import setup_logger


logger = setup_logger("ingest_logger", "ingest.log")

def fetch_fmp_data(endpoint: str, params: dict) -> list:
    url = f"{BASE_URL}/{endpoint}"
    params['apikey'] = FMP_API_KEY

    logger.info(f"Fetching data from FMP API: {url} with params {params}")  
    response = requests.get(url, params=params, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(f"FMP API error {response.status_code}: {response.text}")
    
    logger.info(f"Data fetched successfully from {endpoint}")
    logger.info(f"Response Data: {response.text[:500]}...")  # Log first 500 chars of response
    return response.json()


def save_raw_data(data: list, filename: str) -> None:
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = raw_dir / f"{filename}_{timestamp}.json"
    
    with open(filepath, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Raw data saved to {filepath}")

def ingest(endpoint: str, symbol: str, limit: int = 5) -> None:

    logger.info(f"Starting ingestion for {symbol} - {endpoint}")
    data = fetch_fmp_data(
        endpoint=endpoint,
        params={"symbol": symbol, "limit": limit}
    )
    
    save_raw_data(data, f"{symbol}_{endpoint}")
    logger.info(f"Ingestion completed for {symbol} - {endpoint}")



def main():
    logger.info("Ingestion process started.")
    ingest("income-statement", "WMT", limit=5)  # Ingest last 10 income statements for Walmart
    ingest("balance-sheet-statement", "WMT", limit=5)  # Ingest last 10 balance sheets for Walmart
    ingest("cash-flow-statement", "WMT", limit=5)  # Ingest last 10 cash flow statements for Walmart
    logger.info("Ingestion process completed.")

if __name__ == "__main__":    
    main()