from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Some fields will be null=True, while I will create normal signup/update view
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trips = models.ManyToManyField('trips.TripDate', related_name='account')
    photo = models.ImageField(upload_to='users/photos/', blank=True)
    address = models.TextField(max_length=250, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    passport_number = models.CharField(max_length=20, blank=True)
    passport_nationality = models.CharField(max_length=30, blank=True)
    passport_issue_date = models.DateField(null=True, blank=True)
    passport_expire_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    is_membership = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class UserStripe(models.Model):
    user = models.OneToOneField(Account, on_delete=models.PROTECT, related_name='stripe_account')
    customer_id = models.CharField(max_length=50)

    def __str__(self):
        return self.customer_id


@receiver(post_save, sender=User)
def update_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
    instance.account.save()
