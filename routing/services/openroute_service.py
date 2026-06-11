import os
import requests


class OpenRouteService:

    BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

    def __init__(self):
        self.api_key = os.getenv("OPENROUTE_API_KEY")

    def get_route(self, start_coords, end_coords):
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "coordinates": [
                start_coords,
                end_coords
            ]
        }

        response = requests.post(
            self.BASE_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()