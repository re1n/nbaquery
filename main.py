import requests
import json
import pprint

# Set the API endpoint and headers
endpoint = "https://api.statmuse.com/v1/stats/nba/player"
headers = {
    "Authorization": "Bearer API_KEY",
    "Content-Type": "application/json"
}

# Define a function to get the stats for a player
def get_player_stats(player_name):
    # Set the query parameters
    params = {
        "search": player_name,
        "type": "season",
        "seasonType": "regular",
        "perMode": "totals"
    }

    # Send the request to the API endpoint
    response = requests.get(endpoint, headers=headers, params=params)

    # Convert the response to JSON format
    data = json.loads(response.text)

    # Print the stats for the player
    pprint.pprint(data["totals"])

# Ask the user for a player name
player_name = input("Enter a player name: ")

# Get the stats for the player
get_player_stats(player_name)
