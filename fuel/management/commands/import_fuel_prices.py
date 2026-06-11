from decimal import Decimal
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand

from fuel.models import FuelStation


class Command(BaseCommand):
    help = "Import fuel stations from CSV"

    def handle(self, *args, **kwargs):
        csv_path = Path("data") / "fuel-prices-for-be-assessment.csv"

        if not csv_path.exists():
            self.stdout.write(
                self.style.ERROR(f"CSV not found: {csv_path}")
            )
            return

        df = pd.read_csv(csv_path)

        stations = []

        for _, row in df.iterrows():
            stations.append(
                FuelStation(
                    opis_truckstop_id=int(row["OPIS Truckstop ID"]),
                    truckstop_name=str(row["Truckstop Name"]).strip(),
                    address=str(row["Address"]).strip(),
                    city=str(row["City"]).strip(),
                    state=str(row["State"]).strip(),
                    rack_id=int(row["Rack ID"]) if pd.notna(row["Rack ID"]) else None,
                    retail_price=Decimal(str(row["Retail Price"]))
                )
            )

        FuelStation.objects.bulk_create(
            stations,
            batch_size=1000
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(stations)} stations"
            )
        )