# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-29 12:04
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_auto_20170605_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='Excursion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('duration', models.PositiveSmallIntegerField(blank=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('image', models.ImageField(upload_to='excursions/images/')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trips.Trip')),
            ],
        ),
    ]