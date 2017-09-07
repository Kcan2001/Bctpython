from django.db import models
from tinymce.models import HTMLField


class Trip(models.Model):
    title = models.CharField(max_length=120)
    description = HTMLField()

    def __str__(self):
        return self.title


class TripDate(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT, related_name='trip_date')
    arrival = models.DateField(blank=True)
    departure = models.DateField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return '%s - %s - %s' % (self.trip.title, self.arrival, self.departure)


class TripImage(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT, related_name='trip_image')
    image = models.ImageField(upload_to='trips/images/')
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.trip.title


class Excursion(models.Model):
    title = models.CharField(max_length=100)
    trip = models.ManyToManyField(TripDate, related_name='excursions')
    duration = models.PositiveSmallIntegerField(blank=True)
    description = HTMLField()
    image = models.ImageField(upload_to='excursions/images/')

    def __str__(self):
        return self.title
