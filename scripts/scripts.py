import requests
import pandas as pd

# 1. Get access token
def get_access_token(api_key, api_secret):
    """
    Request an OAuth2 access token from the Amadeus API.

    The access token is required for authenticating subsequent API calls 
    (e.g., flight search). Tokens are short-lived and typically expire 
    within 30 minutes, so this function should be called whenever a 
    new token is needed.

    Args:
        api_key (str): Your permanent Amadeus API key (client_id).
        api_secret (str): Your permanent Amadeus API secret (client_secret).

    Returns:
        str: A short-lived bearer access token for authenticating API requests.

    Example:
        >>> token = get_access_token(API_KEY, API_SECRET)
        >>> print(token)
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    """
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret
    }
    response = requests.post(url, data=data)
    return response.json()["access_token"]

# 2 Get flights for day
def get_flights_for_day(access_token, origin, destination, departure_date, max_results=40):
    '''
    Query the Amadeus API for available flights on a given date and return the results 
    as a DataFrame.

    Args:
        access_token (str): Bearer token from Amadeus for API authentication.
        origin (str): IATA code of the departure airport (e.g., "IAH").
        destination (str): IATA code of the arrival airport (e.g., "JFK").
        departure_date (str): Date of departure in YYYY-MM-DD format.
        max_results (int, optional): Maximum number of flight offers to return. Defaults to 40.

     Returns:
        pandas.DataFrame: A DataFrame where each row represents a flight segment, 
        including airline, flight number, departure/arrival details, duration, and price.

    Example:
        >>> df = get_flights_for_day(token, "IAH", "JFK", "2025-10-15", max_results=3)
        >>> df.head()
    '''
    
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": 1,
        "nonStop": "false",
        "max": max_results
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # raises HTTPError for 4xx/5xx
        flights = response.json()
    except requests.exceptions.RequestExceptions as e:
        print("f ❌ Request failed: {e}")
        return pd.DataFrame()
    except ValueError:
        print("❌ Failed to decode JSON response")
        return pd.DataFrame()

    # Debug info
    if "errors" in flights:
      print("⚠️ API returned errors:")
      print(json.dumps(flights['errors'], index=1))
      return pd.DataFrame()
    if not flights.get('data'):
      print("⚠️ No flight data returned for this query")
      return pd.DataFrame()

    search_date = datetime.now().strftime('%Y-%m-%d') # Today’s date when I pulled the data
    rows = []
    for offer in flights.get("data", []):
        price = offer["price"]["total"]
        for itinerary in offer["itineraries"]:
            duration = itinerary["duration"]
            for segment in itinerary["segments"]:
                rows.append({
                    "OfferID": offer["id"],
                    "Airline": segment["carrierCode"],
                    "Flight": segment["number"],
                    "From": segment["departure"]["iataCode"],
                    "Departure": segment["departure"]["at"],
                    "To": segment["arrival"]["iataCode"],
                    "Arrival": segment["arrival"]["at"],
                    "Duration": duration,
                    "Price": price,
                    'Cabin': segment['cabinClass'],
                    "DepartureDate": departure_date,
                    "SearchDate" : search_date
                })
    return pd.DataFrame(rows)

# 3 Get flights over range
from datetime import datetime, timedelta
import time

def get_flights_over_range(access_token, origin, destination, start_date, end_date, max_results=40):
    """
    Fetch flight offers for every day in a given date range.

    Args:
        access_token (str): Short-lived token from Amadeus for API calls.
        origin (str): IATA code of the departure airport.
        destination (str): IATA code of the arrival airport.
        start_date (str): Start of the date range in YYYY-MM-DD format.
        end_date (str): End of the date range in YYYY-MM-DD format.
        max_results (int, optional): Max results per day. Defaults to 5.

    Returns:
        pandas.DataFrame: Combined DataFrame of all flight offers across the date range.
    """
    # Convert input strings to datetime objects
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    all_flights = []

    current_date = start
    while current_date <= end:
        # Print current date being fetched
        print(f"Fetching: {current_date.strftime('%Y-%m-%d')}")
        # Call your existing function
        flights_df = get_flights_for_day(
            access_token,
            origin,
            destination,
            current_date.strftime("%Y-%m-%d"),
            max_results=max_results
        )

        if not flights_df.empty:
            all_flights.append(flights_df)

        # Move to the next day
        current_date += timedelta(days=1)
        # pause 1 second between API calls
        time.sleep(1) 

    if all_flights:
        return pd.concat(all_flights, ignore_index=True)
    else:
        return pd.DataFrame()

import asyncio
import aiohttp
import pandas as pd
from datetime import datetime, timedelta
import time

async def fetch_flights(session, access_token, origin, destination, date, max_results=5):
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": 1,
        "nonStop": "false",
        "max": max_results
    }
    
    try:
        async with session.get(url, headers=headers, params=params) as resp:
            data = await resp.json()
            if "errors" in data:
                print(f"⚠️ API error for {date}: {data['errors']}")
                return pd.DataFrame()
            rows = []
            for offer in data.get("data", []):
                price = offer["price"]["total"]
                for itinerary in offer["itineraries"]:
                    duration = itinerary["duration"]
                    for segment in itinerary["segments"]:
                        rows.append({
                            "Airline": segment["carrierCode"],
                            "Flight": segment["number"],
                            "From": segment["departure"]["iataCode"],
                            "Departure": segment["departure"]["at"],
                            "To": segment["arrival"]["iataCode"],
                            "Arrival": segment["arrival"]["at"],
                            "Duration": duration,
                            "Price": price,
                            "DepartureDate": date,
                            "SearchDate": datetime.now().strftime("%Y-%m-%d")
                        })
            return pd.DataFrame(rows)
    except Exception as e:
        print(f"❌ Request failed for {date}: {e}")
        return pd.DataFrame()

async def get_flights_over_range_async(access_token, origin, destination, start_date, end_date, max_results=5, delay=1):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
    
    all_flights = []
    
    async with aiohttp.ClientSession() as session:
        for date in dates:
            df = await fetch_flights(session, access_token, origin, destination, date, max_results)
            if not df.empty:
                all_flights.append(df)
            await asyncio.sleep(delay)  # respect rate limit
    
    if all_flights:
        return pd.concat(all_flights, ignore_index=True)
    else:
        return pd.DataFrame()
