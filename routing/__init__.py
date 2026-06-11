import requests


class GeocodingService:
    BASE_URL = "https://nominatim.openstreetmap.org/search"

    def get_coordinates(self, location):
        response = requests.get(
            self.BASE_URL,
            params={
                "q": location,
                "format": "json",
                "limit": 1
            },
            headers={
                "User-Agent": "FuelRouteOptimizer"
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            raise Exception(
                f"Location not found: {location}"
            )

        return [
            float(data[0]["lon"]),
            float(data[0]["lat"])
        ]