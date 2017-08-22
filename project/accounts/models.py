from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Some fields will be null=True, while I will create normal signup/update view
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
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
    instance.account.save()
