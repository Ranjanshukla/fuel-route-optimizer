from fuel.models import FuelStation


class FuelOptimizer:

    MAX_RANGE_MILES = 500
    MPG = 10

    def get_required_stops(self, distance_miles):
        return max(1, int(distance_miles // self.MAX_RANGE_MILES))

    def get_total_gallons(self, distance_miles):
        return round(distance_miles / self.MPG, 2)

    def get_recommended_stations(
        self,
        stop_count,
        start_location,
        destination_location
    ):

        states = set()

        try:
            start_state = start_location.split(",")[-1].strip()
            end_state = destination_location.split(",")[-1].strip()

            states.add(start_state)
            states.add(end_state)

        except Exception:
            pass

        stations = FuelStation.objects.all()

        if states:
            filtered = stations.filter(
                state__in=states
            ).order_by("retail_price")

            if filtered.exists():
                return list(filtered[:stop_count])

        return list(
            stations.order_by("retail_price")[:stop_count]
        )

    def calculate_total_cost(
        self,
        distance_miles,
        fuel_price
    ):
        gallons = distance_miles / self.MPG

        return round(
            gallons * float(fuel_price),
            2
        )