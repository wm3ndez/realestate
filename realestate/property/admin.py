from models import *
from django.contrib import admin
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.admin import AdminImageMixin

class ImagenAdmin(admin.ModelAdmin):
    def titulo_Friendly(self, object):
        return object.titulo

    def imagen_miniatura(self, object):
        image = get_thumbnail(object.imagen, '75x50', crop='center', quality=99)
        return '<img src="%s" />' % image.url

    imagen_miniatura.short_description = "Imagen"
    imagen_miniatura.allow_tags = True
    titulo_Friendly.short_description = "Titulo de la Imagen"

    list_display = ('propiedad', 'imagen_miniatura', 'titulo_Friendly', 'orden')
    search_fields = ['propiedad', 'titulo']
    date_hierarchy = 'agregada'


class ImagenPropiedadInline(AdminImageMixin, admin.TabularInline):
    model = Imagen_Propiedad


class PropiedadAdmin(admin.ModelAdmin):
    # Esto hace que los unicos campos a mostrar sean los siguientes:
    change_form_template = "admin/realestate/propiedad/change_form.html"

    fieldsets = [
        ("Descripcion de la Propiedad",
             {
             'fields': ['titulo', 'slug', 'descripcion', ('precio', 'sector', 'agente'), ('tipo', 'oferta', 'estado')]})
        ,
        ('Detalles',
             {
             #'classes': ('collapse',),
             'fields': [('tamano_solar', 'tamano_construccion'), ('niveles', 'dormitorios', 'banios'),
                 ('marquesina', 'parqueo_techado', 'balcon'), ( 'servicio', 'intercom', 'piscina'),
                 ( 'cocina', 'comedor'), 'coordenadas', 'notas']
         }
            )
    ]

    inlines = [
        ImagenPropiedadInline,
        ]

    list_display = ('titulo_Friendly', 'estado', 'tipo', 'sector', 'agente', 'creacion', 'imagen_miniatura')
    search_fields = ['titulo']
    list_filter = ['creacion', 'agente', 'titulo', 'estado']
    date_hierarchy = 'creacion'

    def titulo_Friendly(self, object):
        return object.titulo

    def imagen_miniatura(self, object):
        imageobj = object.imagen_principal()
        if imageobj:
            image = get_thumbnail(imageobj.imagen, '75x50', quality=99)
            return '<img src="%s" />' % image.url
        else:
            return u'Esta propiedad no contiene imagenes'

    imagen_miniatura.short_description = "Imagen"
    imagen_miniatura.allow_tags = True

    titulo_Friendly.short_description = "Titulo de la Propiedad"


    class Media:
        js = ('js/admin/propiedades.js',)


class EspecialAdmin(admin.ModelAdmin):
    list_display = ('prodiedad', 'estado')


class AgenteAdmin(admin.ModelAdmin):
    list_display = ('agente', 'telefono', 'celular', 'imagen')

    def agente(self, agente):
        return agente.__unicode__()

    agente.short_description = u'Agente Vendedor'

    def imagen(self, object):
        imageobj = object.fotografia
        if imageobj:
            image = get_thumbnail(imageobj, '133x100', quality=99)
            return '<img src="%s" />' % image.url
        else:
            return u'Por favor, agregue una imagen.'

    imagen.short_description = u'Fotografia'
    imagen.allow_tags = True


admin.site.register(Propiedad, PropiedadAdmin)
admin.site.register(Sector)
admin.site.register(Ciudad)
admin.site.register(Agente, AgenteAdmin)
admin.site.register(Imagen_Propiedad, ImagenAdmin)
admin.site.register(Especial)
