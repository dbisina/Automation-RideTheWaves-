from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("API_KEY")


def towns_around_x(town_of_consideration, radius):
    # Get coordinates of reference town using Geocoding API
    geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={town_of_consideration}&key={api_key}"
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()

    # Extract reference town coordinates if successful
    if geocoding_data["status"] == "OK":
        ref_lat = geocoding_data["results"][0]["geometry"]["location"]["lat"]
        ref_lon = geocoding_data["results"][0]["geometry"]["location"]["lng"]
    else:
        print("Error: Could not get coordinates for reference town")
        exit()

    # Google Places API endpoint for text search
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword='town hall'&location={ref_lat},{ref_lon}&radius={radius}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    # Extract potential town information
    potential_towns = []

    if data["status"] == "OK":
        for result in data["results"]:
            plus_code = result.get("plus_code", {})
            compound_code = plus_code.get("compound_code")

            if compound_code:
                # Extract the last 3 words separated by commas
                last_words = compound_code.split(",")[-3:]
                potential_towns.append(
                    " ".join(last_words)
                )  # Join them back with spaces

    # Extract only the desired information (last 3 words)
    towns = [
        town.split()[-3:] for town in potential_towns
    ]  # Get last 3 words for each town

    formatted_towns = []
    for town in towns:
        town_name, state, country = town  # Assign the last 3 words to variables
        formatted_towns.append({"town": town_name, "state": state, "country": country})
        
    return formatted_towns
