{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPbl4A4oMqF3jg/arth9t8V"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "id": "Uhh2MwhjAlYB"
      },
      "outputs": [],
      "source": [
        "import requests\n",
        "import pandas as pd\n",
        "\n",
        "def get_flights_for_day(access_token, origin, destination, departure_date, max_results=5):\n",
        "    url = \"https://test.api.amadeus.com/v2/shopping/flight-offers\"\n",
        "    headers = {\"Authorization\": f\"Bearer {access_token}\"}\n",
        "    params = {\n",
        "        \"originLocationCode\": origin,\n",
        "        \"destinationLocationCode\": destination,\n",
        "        \"departureDate\": departure_date,\n",
        "        \"adults\": 1,\n",
        "        \"nonStop\": \"false\",\n",
        "        \"max\": max_results\n",
        "    }\n",
        "\n",
        "    response = requests.get(url, headers=headers, params=params)\n",
        "    flights = response.json()\n",
        "\n",
        "    rows = []\n",
        "    for offer in flights.get(\"data\", []):\n",
        "        price = offer[\"price\"][\"total\"]\n",
        "        for itinerary in offer[\"itineraries\"]:\n",
        "            duration = itinerary[\"duration\"]\n",
        "            for segment in itinerary[\"segments\"]:\n",
        "                rows.append({\n",
        "                    \"Airline\": segment[\"carrierCode\"],\n",
        "                    \"Flight\": segment[\"number\"],\n",
        "                    \"From\": segment[\"departure\"][\"iataCode\"],\n",
        "                    \"Departure\": segment[\"departure\"][\"at\"],\n",
        "                    \"To\": segment[\"arrival\"][\"iataCode\"],\n",
        "                    \"Arrival\": segment[\"arrival\"][\"at\"],\n",
        "                    \"Duration\": duration,\n",
        "                    \"Price\": price,\n",
        "                    \"SearchDate\": departure_date\n",
        "                })\n",
        "    return pd.DataFrame(rows)\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "J1HlWZNKFT36"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}