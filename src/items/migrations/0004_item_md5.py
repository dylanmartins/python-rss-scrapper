# Generated by Django 3.1.4 on 2020-12-22 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_item_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='md5',
            field=models.CharField(blank=True, editable=False, max_length=16),
        ),
    ]
