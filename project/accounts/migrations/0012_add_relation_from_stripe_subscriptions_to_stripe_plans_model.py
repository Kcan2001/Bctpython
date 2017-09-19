# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-19 08:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_add_stripe_plans_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstripesubscription',
            name='plan',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='stripe_plan_subscription', to='accounts.StripePlanNames'),
            preserve_default=False,
        ),
    ]
