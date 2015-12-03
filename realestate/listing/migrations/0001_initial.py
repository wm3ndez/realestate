# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
from decimal import Decimal
from django.conf import settings
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='First name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last name')),
                ('phone', models.CharField(max_length=15, null=True, verbose_name='Phone', blank=True)),
                ('mobile', models.CharField(max_length=15, null=True, verbose_name='Cellphone', blank=True)),
                ('address', models.CharField(max_length=200, null=True, verbose_name='Address', blank=True)),
                ('image', sorl.thumbnail.fields.ImageField(default=b'', upload_to=b'agents/', null=True, verbose_name='Picture', blank=True)),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Agent',
                'verbose_name_plural': 'Agents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Attribute')),
                ('validation', models.CharField(max_length=100, verbose_name='Value type', choices=[(b'realestate.listing.utils.validation_simple', 'One or more characters'), (b'realestate.listing.utils.validation_integer', 'Integer'), (b'realestate.listing.utils.validation_yesno', 'Yes/No'), (b'realestate.listing.utils.validation_decimal', 'Decimal')])),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Attribute',
                'verbose_name_plural': 'Attributes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttributeListing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('order', models.SmallIntegerField(default=99, verbose_name='Order')),
                ('attribute', models.ForeignKey(to='listing.Attribute')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Listing attribute',
                'verbose_name_plural': 'Listing attributes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price_currency', djmoney.models.fields.CurrencyField(default='XYZ', max_length=3, editable=False, choices=[(b'DOP', 'Dominican Peso'), (b'EUR', 'Euro'), (b'USD', 'US Dollar'), (b'CNY', 'Yuan Renminbi')])),
                ('price', djmoney.models.fields.MoneyField(default=Decimal('0'), verbose_name='Sale Price', max_digits=12, decimal_places=2)),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('start_date', models.DateTimeField(verbose_name='Activation date')),
                ('end_date', models.DateTimeField(verbose_name='Deactivation date')),
            ],
            options={
                'verbose_name': 'Deal',
                'verbose_name_plural': 'Deals',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('price_currency', djmoney.models.fields.CurrencyField(default='XYZ', max_length=3, editable=False, choices=[(b'DOP', 'Dominican Peso'), (b'EUR', 'Euro'), (b'USD', 'US Dollar'), (b'CNY', 'Yuan Renminbi')])),
                ('price', djmoney.models.fields.MoneyField(default=Decimal('0'), verbose_name='Price', max_digits=12, decimal_places=2)),
                ('type', models.CharField(max_length=30, verbose_name='Listing Type', choices=[(b'house', 'Houses'), (b'villa', 'Villas'), (b'penthouse', 'Penthouses'), (b'apartment', 'Apartments'), (b'residencial-land', 'Residential Land'), (b'corporate-office', 'Corporate Offices'), (b'commercial-office', 'Commercial Offices'), (b'commercial-space', 'Commercial Space'), (b'industrial-building', 'Industrial Buildings'), (b'commercial-warehouses', 'Commercial Warehouses'), (b'commercial-land', 'Commercial Land')])),
                ('offer', models.CharField(max_length=10, verbose_name='Offer', choices=[(b'buy', 'For Sale'), (b'rent', 'For Rent'), (b'buy-rent', 'For Sale/For Rent')])),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('baths', models.PositiveIntegerField(default=0, null=True, verbose_name='Bathrooms', blank=True)),
                ('beds', models.PositiveIntegerField(default=0, null=True, verbose_name='Bedrooms', blank=True)),
                ('size', models.PositiveIntegerField(default=0, null=True, verbose_name='Size(m2)', blank=True)),
                ('coords', models.CharField(default=b'19.000000,-70.400000', max_length=255, null=True, verbose_name='Coords', blank=True)),
                ('notes', models.TextField(max_length=500, null=True, verbose_name='Private Notes', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('agent', models.ForeignKey(verbose_name='Agent', blank=True, to='listing.Agent', null=True)),
                ('contact', models.ForeignKey(blank=True, to='home.Contact', null=True)),
            ],
            options={
                'ordering': ['-pk'],
                'verbose_name': 'Listing',
                'verbose_name_plural': 'Listings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name='Name')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'listing/', verbose_name='Image')),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='Added')),
                ('order', models.IntegerField(default=99, max_length=2, null=True, verbose_name='Order')),
                ('listing', models.ForeignKey(related_name='images', verbose_name='Listing', to='listing.Listing')),
            ],
            options={
                'verbose_name': 'Picture',
                'verbose_name_plural': 'Pictures',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name='Name')),
                ('location_type', models.CharField(default=b'sector', max_length=20, verbose_name='Location Type', choices=[(b'street', 'Street'), (b'sector', 'Sector'), (b'city', 'City'), (b'state', 'State/Province')])),
                ('parent', models.ForeignKey(verbose_name='Location', blank=True, to='listing.Location', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='listing',
            name='location',
            field=models.ForeignKey(blank=True, to='listing.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deal',
            name='listing',
            field=models.ForeignKey(verbose_name='Listing', to='listing.Listing'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attributelisting',
            name='listing',
            field=models.ForeignKey(to='listing.Listing'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='location',
            field=models.ForeignKey(verbose_name='Location', blank=True, to='listing.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='User'),
            preserve_default=True,
        ),
    ]
