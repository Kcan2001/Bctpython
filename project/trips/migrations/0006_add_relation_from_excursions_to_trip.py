# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-02 09:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0005_trip_model_changes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excursion',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='excursions', to='trips.Trip'),
        ),
    ]