# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, upload_to='agents/', verbose_name='Picture', default='', null=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='validation',
            field=models.CharField(choices=[('realestate.listing.utils.validation_simple', 'One or more characters'), ('realestate.listing.utils.validation_integer', 'Integer'), ('realestate.listing.utils.validation_yesno', 'Yes/No'), ('realestate.listing.utils.validation_decimal', 'Decimal')], verbose_name='Value type', max_length=100),
        ),
        migrations.AlterField(
            model_name='listing',
            name='coords',
            field=models.CharField(max_length=255, null=True, verbose_name='Coords', default='19.000000,-70.400000', blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='offer',
            field=models.CharField(choices=[('buy', 'For Sale'), ('rent', 'For Rent'), ('buy-rent', 'For Sale/For Rent')], verbose_name='Offer', max_length=10),
        ),
        migrations.AlterField(
            model_name='listing',
            name='type',
            field=models.CharField(choices=[('house', 'Houses'), ('villa', 'Villas'), ('penthouse', 'Penthouses'), ('apartment', 'Apartments'), ('residencial-land', 'Residential Land'), ('corporate-office', 'Corporate Offices'), ('commercial-office', 'Commercial Offices'), ('commercial-space', 'Commercial Space'), ('industrial-building', 'Industrial Buildings'), ('commercial-warehouses', 'Commercial Warehouses'), ('commercial-land', 'Commercial Land')], verbose_name='Listing Type', max_length=30),
        ),
        migrations.AlterField(
            model_name='listingimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to='listing/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='listingimage',
            name='order',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Order', default=99),
        ),
        migrations.AlterField(
            model_name='location',
            name='location_type',
            field=models.CharField(choices=[('street', 'Street'), ('sector', 'Sector'), ('city', 'City'), ('state', 'State/Province')], verbose_name='Location Type', default='sector', max_length=20),
        ),
    ]
