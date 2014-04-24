from django.forms import ValidationError
from django.forms.models import ModelForm
from realestate.property.models import PropertyImage, AttributeProperty, Property, Sector, Ciudad, Agent, OnSale, \
    Attribute
from django.contrib import admin
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.admin import AdminImageMixin
from realestate.property.templatetags.extra_functions import currency
from realestate.property.utils import import_validator, validate_attribute_value


class ImagenAdmin(admin.ModelAdmin):
    def titulo_Friendly(self, obj):
        return obj.titulo

    def imagen_miniatura(self, obj):
        image = get_thumbnail(obj.imagen, '75x50', crop='center', quality=99)
        return '<img src="%s" />' % image.url

    imagen_miniatura.short_description = "Imagen"
    imagen_miniatura.allow_tags = True
    titulo_Friendly.short_description = "Titulo de la Imagen"

    list_display = ('property_item', 'imagen_miniatura', 'titulo_Friendly', 'order')
    search_fields = ['property_item', 'title']
    date_hierarchy = 'added'


def clean_attribute_value(cleaned_data):
    value = cleaned_data['value']
    attribute = cleaned_data['attribute']
    obj = cleaned_data['property']
    success, valid_value, error_message = validate_attribute_value(attribute, value, obj)

    if not success:
        raise ValidationError(error_message)
    return valid_value


class ImagenPropiedadInline(AdminImageMixin, admin.TabularInline):
    model = PropertyImage


class AtributosPropiedadInlineForm(ModelForm):
    def clean_value(self):
        return clean_attribute_value(self.cleaned_data)


class AtributosPropiedadInline(admin.TabularInline):
    model = AttributeProperty
    form = AtributosPropiedadInlineForm


class PropiedadAdmin(admin.ModelAdmin):
    change_form_template = "admin/realestate/property/change_form.html"
    fieldsets = [
        ("Descripcion de la Propiedad",
         {
             'fields': [
                 'title', 'description', 'price', ( 'baths', 'beds', 'size'), 'sector', 'type', 'offer',
                 'status', 'featured', 'frontpage',
             ]
         }),
        ('Detalles',
         {
             'fields': [
                 'agent', 'contact', 'notes', 'coords',
             ]
         })
    ]

    inlines = [AtributosPropiedadInline, ImagenPropiedadInline, ]

    list_display = (
        'id', 'title', 'slug', 'currency_price', 'status', 'type', 'ciudad', 'sector', 'agent', 'created_at',
        'featured', 'imagen_miniatura'
    )

    def currency_price(self, property):
        return currency(property.price)

    currency_price.short_description = u'Precio'

    list_display_links = ('id', 'title')
    search_fields = ['title', 'sector__ciudad']
    list_filter = ['created_at', 'agent', 'title', 'status', ]
    date_hierarchy = 'created_at'

    def ciudad(self, propiedad):
        if propiedad.sector is None:
            return u'(No seleccionada)'
        return '%s, %s' % (propiedad.sector.ciudad, propiedad.sector.ciudad.provincia)

    def imagen_miniatura(self, obj):
        imageobj = obj.main_image
        if imageobj:
            image = get_thumbnail(imageobj.image, '75x50', quality=99)
            return '<img src="%s" />' % image.url
        else:
            return u'Esta property no contiene imagenes'

    imagen_miniatura.short_description = "Imagen"
    imagen_miniatura.allow_tags = True

    class Media:
        js = ('js/admin/propiedades.js',)


class EspecialAdmin(admin.ModelAdmin):
    list_display = ('prodiedad', 'status')


class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'telefono', 'celular', 'image')

    def agente(self, agente):
        return agente.__unicode__()

    agente.short_description = u'Agente Vendedor'

    def imagen(self, obj):
        imageobj = obj.fotografia
        if imageobj:
            image = get_thumbnail(imageobj, '133x100', quality=99)
            return '<img src="%s" />' % image.url
        else:
            return u'Por favor, agregue una image.'

    imagen.short_description = u'Fotografia'
    imagen.allow_tags = True


class AtributosForm(ModelForm):
    def clean_validation(self):
        validation = self.cleaned_data['validation']
        try:
            import_validator(validation)
        except ImportError:
            raise ValidationError(_("Invalid validation function specifed!"))
        return validation


class AttributesAdmin(admin.ModelAdmin):
    form = AtributosForm


admin.site.register(Property, PropiedadAdmin)
admin.site.register(Sector)
admin.site.register(Ciudad)
admin.site.register(Agent, AgentAdmin)
admin.site.register(PropertyImage, ImagenAdmin)
admin.site.register(OnSale)
admin.site.register(Attribute, AttributesAdmin)
