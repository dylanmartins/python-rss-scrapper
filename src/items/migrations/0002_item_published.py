# Generated by Django 3.1.4 on 2020-12-21 23:37

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='published',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
