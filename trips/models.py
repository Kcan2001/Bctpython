from django.db import models


class Trip(models.Model):
    title = models.CharField(max_length=120, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    slug = models.SlugField(unique=True)
    arrival = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    departure = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    def __str__(self):
        return self.title

class TripImage(models.Model):
    trip = models.ForeignKey(Trip)
    image = models.ImageField(upload_to='trips/images/')
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.trip.title

# Create your models here.
