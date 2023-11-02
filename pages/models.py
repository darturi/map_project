import geocoder
from django.urls import reverse
from django.conf import settings
from environs import Env


# from django.contrib.postgres.fields import ArrayField


from django.db import models

env = Env()
env.read_env()
mapbox_access_token = env.str("MAPBOX_ACCESS_TOKEN")


class Address(models.Model):
    address = models.TextField()
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    description = models.CharField(
        max_length=140, null=True
    )  # This is gonna show for all users
    # saved_by = ArrayField(models.ForeignKey(settings.AUTH_USER_MODEL))

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_access_token)
        g = g.latlng  # returns => [lat, long]
        self.lat = g[0]
        self.long = g[1]
        return super(Address, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.address

    def get_absolute_url(self):
        return reverse("address_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    comment = models.CharField(max_length=140)
    date = models.DateTimeField(auto_now_add=True, null=True)

    # parent = models.ForeignKey(Address, on_delete=models.CASCADE)

    # Will return the comment content as a string
    def __str__(self):
        return self.comment

    # Will return the url associated with "profile"
    def get_absolute_url(self):
        return reverse("profile")


class SavedPin(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_access_token)
        g = g.latlng  # returns => [lat, long]
        self.lat = g[0]
        self.long = g[1]
        return super(Address, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.address

    def get_absolute_url(self):
        return reverse("address_detail", kwargs={"pk": self.pk})
