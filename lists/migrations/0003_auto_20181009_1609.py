# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-09 22:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_item_passtext'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='passtext',
            new_name='text',
        ),
    ]