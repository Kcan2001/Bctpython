# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-29 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0005_trip_model_changes'),
        ('accounts', '0003_account_add_email_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='trips',
            field=models.ManyToManyField(to='trips.Trip'),
        ),
    ]