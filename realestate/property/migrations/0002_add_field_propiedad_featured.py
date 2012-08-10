# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Propiedad.featured'
        db.add_column('property_propiedad', 'featured',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Propiedad.featured'
        db.delete_column('property_propiedad', 'featured')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'property.agente': {
            'Meta': {'object_name': 'Agente'},
            'celular': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'ciudad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['property.Ciudad']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'property.ciudad': {
            'Meta': {'object_name': 'Ciudad'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'provincia': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'property.especial': {
            'Meta': {'object_name': 'Especial'},
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'final': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateTimeField', [], {}),
            'propiedad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['property.Propiedad']"})
        },
        'property.imagen_propiedad': {
            'Meta': {'object_name': 'Imagen_Propiedad'},
            'agregada': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'orden': ('django.db.models.fields.IntegerField', [], {'default': '99', 'max_length': '2', 'null': 'True'}),
            'propiedad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['property.Propiedad']"}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'property.propiedad': {
            'Meta': {'object_name': 'Propiedad'},
            'agente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['property.Agente']"}),
            'amueblado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'balcon': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'banios': ('django.db.models.fields.IntegerField', [], {'default': '2', 'max_length': '2'}),
            'cocina': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'comedor': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'coordenadas': ('django.db.models.fields.CharField', [], {'default': "'19.000000,-70.400000'", 'max_length': '22'}),
            'creacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'dormitorios': ('django.db.models.fields.IntegerField', [], {'default': '3', 'max_length': '2'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intercom': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marquesina': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'niveles': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'notas': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'oferta': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'parqueo_techado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'piscina': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '12', 'decimal_places': '2'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['property.Sector']"}),
            'servicio': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'tamano_construccion': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tamano_solar': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'property.sector': {
            'Meta': {'object_name': 'Sector'},
            'ciudad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['property.Ciudad']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        }
    }

    complete_apps = ['property']