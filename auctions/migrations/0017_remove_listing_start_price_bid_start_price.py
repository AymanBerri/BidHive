# Generated by Django 4.1.7 on 2023-07-23 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_rename_price_listing_start_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='start_price',
        ),
        migrations.AddField(
            model_name='bid',
            name='start_price',
            field=models.BooleanField(default=False),
        ),
    ]
