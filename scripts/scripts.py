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
def get_flights_for_day(access_token, origin, destination, departure_date, max_results=5):
    '''
    Query the Amadeus API for available flights on a given date and return the results 
    as a DataFrame.

    Args:
        access_token (str): Bearer token from Amadeus for API authentication.
        origin (str): IATA code of the departure airport (e.g., "IAH").
        destination (str): IATA code of the arrival airport (e.g., "JFK").
        departure_date (str): Date of departure in YYYY-MM-DD format.
        max_results (int, optional): Maximum number of flight offers to return. Defaults to 5.

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

    response = requests.get(url, headers=headers, params=params)
    flights = response.json()

    rows = []
    for offer in flights.get("data", []):
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
                    "SearchDate": departure_date
                })
    return pd.DataFrame(rows)

