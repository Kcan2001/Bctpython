# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 22:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_tripimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
