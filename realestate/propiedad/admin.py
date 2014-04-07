from django.forms import ValidationError
from django.forms.models import ModelForm
from models import *
from django.contrib import admin
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.admin import AdminImageMixin
from realestate.propiedad.templatetags.extra_functions import currency
from realestate.propiedad.utils import import_validator, validate_attribute_value


class ImagenAdmin(admin.ModelAdmin):
    def titulo_Friendly(self, obj):
        return obj.titulo

    def imagen_miniatura(self, obj):
        image = get_thumbnail(obj.imagen, '75x50', crop='center', quality=99)
        return '<img src="%s" />' % image.url

    imagen_miniatura.short_description = "Imagen"
    imagen_miniatura.allow_tags = True
    titulo_Friendly.short_description = "Titulo de la Imagen"

    list_display = ('propiedad', 'imagen_miniatura', 'titulo_Friendly', 'orden')
    search_fields = ['propiedad', 'titulo']
    date_hierarchy = 'agregada'


def clean_attribute_value(cleaned_data):
    value = cleaned_data['valor']
    attribute = cleaned_data['atributo']
    obj = cleaned_data['propiedad']
    success, valid_value, error_message = validate_attribute_value(attribute, value, obj)

    if not success:
        raise ValidationError(error_message)
    return valid_value


class ImagenPropiedadInline(AdminImageMixin, admin.TabularInline):
    model = Imagen_Propiedad


class AtributosPropiedadInlineForm(ModelForm):
    def clean_value(self):
        return clean_attribute_value(self.cleaned_data)


class AtributosPropiedadInline(admin.TabularInline):
    model = AtributosPropiedad
    form = AtributosPropiedadInlineForm


class PropiedadAdmin(admin.ModelAdmin):
    # Esto hace que los unicos campos a mostrar sean los siguientes:
    change_form_template = "admin/realestate/propiedad/change_form.html"

    fieldsets = [
        ("Descripcion de la Propiedad",
         {
             'fields': [
                 'titulo', 'descripcion', ('precio', 'sector', 'agente'),
                 ('tipo', 'oferta', 'estado', 'featured')
             ]
         }),
        ('Detalles',
         {
             'fields': [
                 ('tamano_solar', 'tamano_construccion'), ('niveles', 'dormitorios', 'banios'),
                 ('marquesina', 'parqueo_techado', 'balcon'), ('servicio', 'intercom', 'piscina'),
                 ('cocina', 'comedor'), 'coordenadas', 'notas'
             ]
         })
    ]

    inlines = [
        ImagenPropiedadInline,
        AtributosPropiedadInline
    ]

    list_display = (
        'id', 'titulo', 'slug', 'currency_price', 'estado', 'tipo', 'ciudad', 'sector', 'agente', 'creacion',
        'featured', 'imagen_miniatura'
    )

    def currency_price(self, propiedad):
        return currency(propiedad.precio)

    currency_price.short_description = u'Precio'

    list_display_links = ('id', 'titulo')
    search_fields = ['titulo', 'sector__ciudad']
    list_filter = ['creacion', 'agente', 'titulo', 'estado', ]
    date_hierarchy = 'creacion'


    def ciudad(self, propiedad):
        return '%s, %s' % (propiedad.sector.ciudad, propiedad.sector.ciudad.provincia )

    def imagen_miniatura(self, obj):
        imageobj = obj.imagen_principal
        if imageobj:
            image = get_thumbnail(imageobj.imagen, '75x50', quality=99)
            return '<img src="%s" />' % image.url
        else:
            return u'Esta propiedad no contiene imagenes'

    imagen_miniatura.short_description = "Imagen"
    imagen_miniatura.allow_tags = True

    class Media:
        js = ('js/admin/propiedades.js',)


class EspecialAdmin(admin.ModelAdmin):
    list_display = ('prodiedad', 'estado')


class AgenteAdmin(admin.ModelAdmin):
    list_display = ('agente', 'telefono', 'celular', 'imagen')

    def agente(self, agente):
        return agente.__unicode__()

    agente.short_description = u'Agente Vendedor'

    def imagen(self, obj):
        imageobj = obj.fotografia
        if imageobj:
            image = get_thumbnail(imageobj, '133x100', quality=99)
            return '<img src="%s" />' % image.url
        else:
            return u'Por favor, agregue una imagen.'

    imagen.short_description = u'Fotografia'
    imagen.allow_tags = True


class AtributosForm(ModelForm):
    def clean_validation(self):
        validation = self.cleaned_data['validacion']
        try:
            import_validator(validation)
        except ImportError:
            raise ValidationError(_("Invalid validation function specifed!"))
        return validation


class AtributosAdmin(admin.ModelAdmin):
    form = AtributosForm


admin.site.register(Propiedad, PropiedadAdmin)
admin.site.register(Sector)
admin.site.register(Ciudad)
admin.site.register(Agente, AgenteAdmin)
admin.site.register(Imagen_Propiedad, ImagenAdmin)
admin.site.register(Especial)
admin.site.register(AtributosAdmin)
