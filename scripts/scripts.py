import requests
import pandas as pd

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

