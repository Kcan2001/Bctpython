from django.db import models
from tinymce.models import HTMLField


class Trip(models.Model):
    title = models.CharField(max_length=120)
    description = HTMLField()
    price = models.DecimalField(decimal_places=2, max_digits=100)
    departure = models.DateTimeField(blank=True)
    arrival = models.DateTimeField(blank=True)

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


class Excursion(models.Model):
    title = models.CharField(max_length=100)
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT, related_name='excursions')
    duration = models.PositiveSmallIntegerField(blank=True)
    description = HTMLField()
    image = models.ImageField(upload_to='excursions/images/')

    def __str__(self):
        return self.title
