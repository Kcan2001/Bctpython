# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-10 15:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_change_ckeditor_to_tinymce'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Account'),
        ),
    ]
