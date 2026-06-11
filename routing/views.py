from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from routing.serializers import RouteRequestSerializer
from routing.services.geocoding_service import GeocodingService
from routing.services.openroute_service import OpenRouteService
from optimizer.services.fuel_optimizer import FuelOptimizer


class OptimizeRouteAPIView(APIView):

    def post(self, request):
        serializer = RouteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:

            start_location = (
                serializer.validated_data["start"]
            )

            destination_location = (
                serializer.validated_data["destination"]
            )

            geo = GeocodingService()

            start_coords = geo.get_coordinates(
                start_location
            )

            end_coords = geo.get_coordinates(
                destination_location
            )

            route = OpenRouteService().get_route(
                start_coords,
                end_coords
            )

            summary = (
                route["routes"][0]["summary"]
            )

            distance_miles = round(
                summary["distance"] * 0.000621371,
                2
            )

            optimizer = FuelOptimizer()

            fuel_stops_required = (
                optimizer.get_required_stops(
                    distance_miles
                )
            )

            stations = (
                optimizer.get_recommended_stations(
                    max(1, fuel_stops_required),
                    route["routes"][0]["geometry"]
                )
            )

            recommended_stations = []

            for station in stations:

                recommended_stations.append({
                    "name": station.truckstop_name,
                    "city": station.city,
                    "state": station.state,
                    "price": float(
                        station.retail_price
                    )
                })

            lowest_price = (
                stations[0].retail_price
                if stations
                else 3.50
            )

            estimated_cost = (
                optimizer.calculate_total_cost(
                    distance_miles,
                    lowest_price
                )
            )

            return Response({
                "start": start_location,
                "destination": destination_location,
                "distance_miles": distance_miles,
                "duration_seconds": summary["duration"],
                "fuel_stops_required": fuel_stops_required,
                "estimated_fuel_cost": estimated_cost,
                "recommended_fuel_stops": recommended_stations,
                "route_geometry": route["routes"][0]["geometry"]
            })

        except Exception as e:
            return Response({"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )