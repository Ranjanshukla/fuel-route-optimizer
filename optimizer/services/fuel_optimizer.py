from math import radians
from math import sin
from math import cos
from math import sqrt
from math import atan2

import polyline

from fuel.models import FuelStation


class FuelOptimizer:

    MAX_RANGE_MILES = 500
    MPG = 10

    def get_required_stops(
        self,
        distance_miles
    ):
        return max(
            1,
            int(
                distance_miles //
                self.MAX_RANGE_MILES
            )
        )

    def get_total_gallons(
        self,
        distance_miles
    ):
        return round(
            distance_miles / self.MPG,
            2
        )

    def haversine_distance(
        self,
        lat1,
        lon1,
        lat2,
        lon2
    ):

        radius = 3958.8

        dlat = radians(
            lat2 - lat1
        )

        dlon = radians(
            lon2 - lon1
        )

        a = (
            sin(dlat / 2) ** 2
            +
            cos(radians(lat1))
            *
            cos(radians(lat2))
            *
            sin(dlon / 2) ** 2
        )

        c = (
            2 *
            atan2(
                sqrt(a),
                sqrt(1 - a)
            )
        )

        return radius * c

    def get_recommended_stations(
        self,
        stop_count,
        route_geometry
    ):

        route_points = polyline.decode(
            route_geometry
        )

        # Reduce processing
        route_points = route_points[::25]

        nearby_stations = []

        stations = (
            FuelStation.objects
            .filter(
                latitude__isnull=False,
                longitude__isnull=False
            )
        )

        for station in stations:

            for (
                route_lat,
                route_lon
            ) in route_points:

                distance = (
                    self.haversine_distance(
                        station.latitude,
                        station.longitude,
                        route_lat,
                        route_lon
                    )
                )

                if distance <= 25:

                    nearby_stations.append(
                        station
                    )

                    break

        nearby_stations = sorted(
            nearby_stations,
            key=lambda x: x.retail_price
        )

        return nearby_stations[
            :stop_count
        ]

    def calculate_total_cost(
        self,
        distance_miles,
        fuel_price
    ):

        gallons = (
            distance_miles /
            self.MPG
        )

        return round(
            gallons *
            float(fuel_price),
            2
        )