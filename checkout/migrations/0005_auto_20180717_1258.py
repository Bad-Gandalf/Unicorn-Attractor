# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-17 12:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_auto_20180716_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlineitem',
            name='feature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='features.Feature'),
        ),
    ]
