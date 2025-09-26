import requests
import pandas as pd

def get_flights_for_day(access_token, origin, destination, departure_date, max_results=5):
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

