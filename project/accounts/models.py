from django.db import models
from django.contrib.auth.models import User

# Some fields will bu null=True, while I will create normal signup/update view
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/photos/', blank=True)
    address = models.TextField(max_length=250, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    passport_number = models.CharField(max_length=20, blank=True)
    passport_nationality = models.CharField(max_length=30, blank=True)
    passport_issue_date = models.DateField(null=True, blank=True)
    passport_expire_date = models.DateField(null=True, blank=True)
