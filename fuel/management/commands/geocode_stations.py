import time
from geopy.geocoders import Nominatim
from geopy.exc import (GeocoderTimedOut, GeocoderServiceError)
from django.core.management.base import BaseCommand
from fuel.models import FuelStation


CANADA_PROVINCES = {
    "ON", "QC", "BC", "AB",
    "MB", "NB", "NL", "NS",
    "PE", "SK", "YT", "NT", "NU"
}


class Command(BaseCommand):
    help = "Geocode fuel stations"

    def handle(self, *args, **kwargs):

        geolocator = Nominatim(
            user_agent="fuel_route_optimizer_v3"
        )

        stations = (
            FuelStation.objects
            .filter(is_geocoded=False)
            .exclude(state__in=CANADA_PROVINCES)
        )

        total = stations.count()

        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write(
            f"Total Pending USA Stations: {total}"
        )
        self.stdout.write("=" * 70)

        success_count = 0
        failed_count = 0

        city_cache = {}

        for index, station in enumerate(
            stations,
            start=1
        ):

            try:

                self.stdout.write("")
                self.stdout.write(
                    f"[{index}/{total}] "
                    f"{station.truckstop_name}"
                )

                city_key = (
                    f"{station.city}|{station.state}"
                )

                # Reuse coordinates if same city already geocoded
                if city_key in city_cache:

                    lat, lon = city_cache[city_key]

                    station.latitude = lat
                    station.longitude = lon
                    station.is_geocoded = True

                    station.save()

                    success_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ CACHE HIT "
                            f"{lat}, {lon}"
                        )
                    )

                else:

                    full_address = (
                        f"{station.address}, "
                        f"{station.city}, "
                        f"{station.state}, USA"
                    )

                    city_state = (
                        f"{station.city}, "
                        f"{station.state}, USA"
                    )

                    location = None

                    # Full address
                    try:

                        location = geolocator.geocode(
                            full_address,
                            timeout=30
                        )

                    except Exception as e:

                        self.stdout.write(
                            self.style.WARNING(
                                f"Full address failed: {e}"
                            )
                        )

                    # Fallback city/state
                    if not location:

                        self.stdout.write(
                            f"Fallback -> {city_state}"
                        )

                        try:

                            location = geolocator.geocode(
                                city_state,
                                timeout=30
                            )

                        except Exception as e:

                            self.stdout.write(
                                self.style.WARNING(
                                    f"Fallback failed: {e}"
                                )
                            )

                    if location:

                        city_cache[city_key] = (
                            location.latitude,
                            location.longitude
                        )

                        station.latitude = (
                            location.latitude
                        )

                        station.longitude = (
                            location.longitude
                        )

                        station.is_geocoded = True

                        station.save()

                        success_count += 1

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"✓ SUCCESS "
                                f"({location.latitude}, "
                                f"{location.longitude})"
                            )
                        )

                    else:

                        failed_count += 1

                        self.stdout.write(
                            self.style.WARNING(
                                "✗ No Result"
                            )
                        )

                        continue

                self.stdout.write(
                    f"Progress => "
                    f"{index}/{total} | "
                    f"Success={success_count} | "
                    f"Failed={failed_count}"
                )

                time.sleep(1)

            except GeocoderTimedOut:

                failed_count += 1

                self.stdout.write(
                    self.style.WARNING(
                        "Timeout"
                    )
                )

            except GeocoderServiceError as e:

                failed_count += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"Service Error: {e}"
                    )
                )

                if "429" in str(e):

                    self.stdout.write(
                        self.style.WARNING(
                            "Sleeping 120 sec..."
                        )
                    )

                    time.sleep(120)

            except Exception as e:

                failed_count += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"Unexpected Error: {e}"
                    )
                )

        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write(
            f"DONE | Success={success_count} "
            f"| Failed={failed_count}"
        )
        self.stdout.write("=" * 70)

