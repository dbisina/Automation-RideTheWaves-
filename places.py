from dotenv import load_dotenv
import os
import requests
from geopy.distance import geodesic
load_dotenv()
api_key = os.getenv("API_KEY")



# Reference town information
reference_town = "Dudley, MA"

# Define search radius in meters (convert miles to meters if needed)
radius = 16093.4

# Google Places API endpoint for text search
url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=towns+near+{reference_town}&radius={radius}&key={api_key}"
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

# List to store nearby towns with distance
nearby_towns = []

# Loop through potential towns and calculate distance
for town_name in potential_towns:
    # Use another Places API request (Details) to get the town's address (consider API limits)
    # ... (code to use Places API Place Details to get the address)
    # Alternatively, assume the town name returned by text search represents the address

    # Calculate distance using geodesic (replace with actual address if available)
    # distance = geodesic((ref_lat, ref_lon), (town_lat, town_lon)).miles
    distance = 0  # Placeholder, replace with actual distance calculation

    # Filter based on distance and name containing "town hall" (case-insensitive)
    if distance <= radius and "town hall" in town_name.lower():
        nearby_towns.append({"name": town_name, "distance": distance})

# Print nearby towns with distance (if any)
if nearby_towns:
    print(f"Nearby towns with town hall within {radius/1000:.2f} km:")
    for town in nearby_towns:
        print(f"\t- {town['name']} (distance: {town['distance']:.2f} km)")
else:
    print("No nearby towns with town hall found within the radius.")
