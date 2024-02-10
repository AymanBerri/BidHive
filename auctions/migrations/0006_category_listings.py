# Generated by Django 4.1.7 on 2023-05-23 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_category_listing_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='listing_categories', to='auctions.listing'),
        ),
    ]
