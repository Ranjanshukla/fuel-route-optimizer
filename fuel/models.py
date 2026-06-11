from django.db import models


class FuelStation(models.Model):
    opis_truckstop_id = models.IntegerField()
    truckstop_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    rack_id = models.IntegerField(null=True,blank=True)
    retail_price = models.DecimalField(max_digits=8, decimal_places=3)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    is_geocoded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "fuel_stations"

    def __str__(self):
        return f"{self.truckstop_name} - {self.city}"
