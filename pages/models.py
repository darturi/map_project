import geocoder
from django.urls import reverse

from django.db import models


mapbox_access_token = "pk.eyJ1IjoiZGFuaWVsYXJ0dXJpIiwiYSI6ImNsbTJ2c2ZrYjF6bHozcm85d3phc2c1bTUifQ.Ubn6vNMeUlWJ4iBomj9_BA"


class Address(models.Model):
    address = models.TextField()
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_access_token)
        g = g.latlng  # returns => [lat, long]
        self.lat = g[0]
        self.long = g[1]
        return super(Address, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.address

    def get_absolute_url(self):
        return reverse("profile")
