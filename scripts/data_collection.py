
# scripts/data_collection.py

"""
Flight Offers Data Collection Script

Fetches flight offers from the Amadeus API using helper functions in scripts.py
and saves the results as a timestamped CSV into data/raw/.
"""

import os
from datetime import datetime
import pandas as pd

# Import your helper functions from scripts/scripts.py
from scripts import get_flights_for_day, get_access_token, get_flights_over_range


def main():
    # --- Authentication ---
    api_key = os.getenv("AMADEUS_KEY")
    api_secret = os.getenv("AMADEUS_SECRET")

    if not api_key or not api_secret:
        raise ValueError("Missing API credentials. Make sure AMADEUS_KEY and AMADEUS_SECRET are set as environment variables.")

    token = get_access_token(api_key, api_secret)

    # --- Fetch flight offers ---
    # Example route/dates — adjust as needed
    origin = "IAH"
    destination = "LAX"
    start_date = "2025-11-15"
    end_date = "2025-12-31"

    df_offers = get_flights_over_range(token, origin, destination, start_date, end_date)
    print(f"Fetched {df_offers.shape[0]} flight offers.")

    # --- Save results ---
    data_path = os.path.join("data", "raw")
    os.makedirs(data_path, exist_ok=True)

    search_date = datetime.utcnow().strftime("%Y-%m-%d")
    file_path = os.path.join(data_path, f"{search_date}.csv")

    df_offers.to_csv(file_path, index=False)
    print(f"Saved CSV to {file_path}")


if __name__ == "__main__":
    main()
