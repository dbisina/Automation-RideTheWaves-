from dotenv import load_dotenv
import os

import requests
from geopy.distance import geodesic

load_dotenv()
api_key = os.getenv("API_KEY")


# Reference town information
reference_town = "Dudley, MA"

# Define search radius in meters (convert miles to meters if needed)
radius = 16000

# Get coordinates of reference town using Geocoding API
geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={reference_town}&key={api_key}"
geocoding_response = requests.get(geocoding_url)
geocoding_data = geocoding_response.json()


# Extract reference town coordinates if successful
if geocoding_data["status"] == "OK":
    ref_lat = geocoding_data["results"][0]["geometry"]["location"]["lat"]
    ref_lon = geocoding_data["results"][0]["geometry"]["location"]["lng"]
else:
    print("Error: Could not get coordinates for reference town")
    exit()

print(ref_lat, ref_lon)

# Google Places API endpoint for text search
url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword='town hall'&location={ref_lat},{ref_lon}&radius={radius}&key={api_key}"
response = requests.get(url)
data = response.json()

# Extract potential town names from search results
potential_towns = []

if data["status"] == "OK":
    for result in data["results"]:
        potential_towns.append(result["name"])
else:
    print("Error: Could not get results from Places API")
    exit()

print(potential_towns)
