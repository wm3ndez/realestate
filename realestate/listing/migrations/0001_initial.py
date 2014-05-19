# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'City'
        db.create_table(u'listing_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal(u'listing', ['City'])

        # Adding model 'Sector'
        db.create_table(u'listing_sector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listing.City'])),
        ))
        db.send_create_signal(u'listing', ['Sector'])

        # Adding model 'Agent'
        db.create_table(u'listing_agent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listing.City'], null=True, blank=True)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(default='', max_length=100, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'listing', ['Agent'])

        # Adding model 'Listing'
        db.create_table(u'listing_listing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('price_currency', self.gf('djmoney.models.fields.CurrencyField')()),
            ('price', self.gf('djmoney.models.fields.MoneyField')(max_digits=12, decimal_places=2, default_currency='XYZ')),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listing.Sector'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('offer', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('baths', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
            ('beds', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
            ('coords', self.gf('django.db.models.fields.CharField')(default='19.000000,-70.400000', max_length=255, null=True, blank=True)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listing.Agent'], null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Contact'], null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'listing', ['Listing'])

        # Adding model 'Attribute'
        db.create_table(u'listing_attribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('validation', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'listing', ['Attribute'])

        # Adding model 'AttributeListing'
        db.create_table(u'listing_attributelisting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('listing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listing.Listing'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listing.Attribute'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'listing', ['AttributeListing'])

        # Adding model 'ListingImage'
        db.create_table(u'listing_listingimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('listing', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['listing.Listing'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=99, max_length=2, null=True)),
        ))
        db.send_create_signal(u'listing', ['ListingImage'])

        # Adding model 'OnSale'
        db.create_table(u'listing_onsale', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('listing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['listing.Listing'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'listing', ['OnSale'])


    def backwards(self, orm):
        # Deleting model 'City'
        db.delete_table(u'listing_city')

        # Deleting model 'Sector'
        db.delete_table(u'listing_sector')

        # Deleting model 'Agent'
        db.delete_table(u'listing_agent')

        # Deleting model 'Listing'
        db.delete_table(u'listing_listing')

        # Deleting model 'Attribute'
        db.delete_table(u'listing_attribute')

        # Deleting model 'AttributeListing'
        db.delete_table(u'listing_attributelisting')

        # Deleting model 'ListingImage'
        db.delete_table(u'listing_listingimage')

        # Deleting model 'OnSale'
        db.delete_table(u'listing_onsale')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'home.contact': {
            'Meta': {'object_name': 'Contact'},
            'cellphone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'listing.agent': {
            'Meta': {'object_name': 'Agent'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listing.City']", 'null': 'True', 'blank': 'True'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'listing.attribute': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Attribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'validation': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'listing.attributelisting': {
            'Meta': {'object_name': 'AttributeListing'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listing.Attribute']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listing.Listing']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'listing.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'listing.listing': {
            'Meta': {'ordering': "['-pk']", 'object_name': 'Listing'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listing.Agent']", 'null': 'True', 'blank': 'True'}),
            'baths': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'beds': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Contact']", 'null': 'True', 'blank': 'True'}),
            'coords': ('django.db.models.fields.CharField', [], {'default': "'19.000000,-70.400000'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'offer': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'price': ('djmoney.models.fields.MoneyField', [], {'max_digits': '12', 'decimal_places': '2', 'default_currency': u"'XYZ'"}),
            'price_currency': ('djmoney.models.fields.CurrencyField', [], {}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listing.Sector']", 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'listing.listingimage': {
            'Meta': {'object_name': 'ListingImage'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['listing.Listing']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '99', 'max_length': '2', 'null': 'True'})
        },
        u'listing.onsale': {
            'Meta': {'object_name': 'OnSale'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listing.Listing']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'listing.sector': {
            'Meta': {'object_name': 'Sector'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['listing.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        }
    }

    complete_apps = ['listing']