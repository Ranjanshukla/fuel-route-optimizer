import os
import requests


class GeocodingService:

    BASE_URL = "https://api.openrouteservice.org/geocode/search"

    def __init__(self):
        self.api_key = os.getenv("OPENROUTE_API_KEY")

    def get_coordinates(self, location):

        response = requests.get(
            self.BASE_URL,
            params={
                "api_key": self.api_key,
                "text": location,
                "size": 1
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        coordinates = (
            data["features"][0]
            ["geometry"]
            ["coordinates"]
        )

        return coordinates