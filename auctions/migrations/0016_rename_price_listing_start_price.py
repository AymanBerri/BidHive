# Generated by Django 4.1.7 on 2023-07-23 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_listing_price_alter_listing_bidding_winner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='price',
            new_name='start_price',
        ),
    ]