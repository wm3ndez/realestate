from django.forms import ValidationError
from django.forms.models import ModelForm
from realestate.listing.models import ListingImage, AttributeListing, Listing, Sector, City, Agent, OnSale, \
    Attribute
from django.contrib import admin
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.admin import AdminImageMixin
from realestate.listing.templatetags.extra_functions import currency
from realestate.listing.utils import import_validator, validate_attribute_value
from django.utils.translation import ugettext as _


class ImagenAdmin(admin.ModelAdmin):
    def titulo_Friendly(self, obj):
        return obj.titulo

    def imagen_miniatura(self, obj):
        image = get_thumbnail(obj.imagen, '75x50', crop='center', quality=99)
        return '<img src="%s" />' % image.url

    imagen_miniatura.short_description = "Imagen"
    imagen_miniatura.allow_tags = True
    titulo_Friendly.short_description = "Titulo de la Imagen"

    list_display = ('listing', 'imagen_miniatura', 'titulo_Friendly', 'order')
    search_fields = ['listing', 'title']
    date_hierarchy = 'added'


def clean_attribute_value(cleaned_data):
    value = cleaned_data['value']
    attribute = cleaned_data['attribute']
    obj = cleaned_data['listing']
    success, valid_value, error_message = validate_attribute_value(attribute, value, obj)

    if not success:
        raise ValidationError(error_message)
    return valid_value


class ImagenPropiedadInline(AdminImageMixin, admin.TabularInline):
    model = ListingImage


class AtributosPropiedadInlineForm(ModelForm):
    def clean_value(self):
        return clean_attribute_value(self.cleaned_data)


class AtributosPropiedadInline(admin.TabularInline):
    model = AttributeListing
    form = AtributosPropiedadInlineForm


class ListingAdmin(admin.ModelAdmin):
    change_form_template = "admin/realestate/listing/change_form.html"
    fieldsets = [
        ("Descripcion de la Propiedad",
         {
             'fields': [
                 'title', 'description', 'price', ( 'baths', 'beds', 'size'), 'sector', 'type', 'offer',
                 'active', 'featured',
             ]
         }),
        (_('Contact Info'),
         {
             'fields': [
                 'agent', 'contact', 'notes', 'coords',
             ]
         })
    ]

    inlines = [AtributosPropiedadInline, ImagenPropiedadInline, ]

    list_display = (
        'id', 'title', 'slug', 'currency_price', 'active', 'type', 'city', 'sector', 'agent', 'created_at',
        'featured', 'imagen_miniatura'
    )

    def currency_price(self, listing):
        return currency(listing.price)

    currency_price.short_description = u'Precio'

    list_display_links = ('id', 'title')
    search_fields = ['title', 'sector__ciudad']
    list_filter = ['created_at', 'agent', 'title', 'active', ]
    date_hierarchy = 'created_at'

    def city(self, listing):
        if listing.sector is None:
            return u'(No seleccionada)'
        return '%s, %s' % (listing.sector.city, listing.sector.city.province)

    def imagen_miniatura(self, obj):
        imageobj = obj.main_image
        if imageobj:
            image = get_thumbnail(imageobj.image, '75x50', quality=99)
            return '<img src="%s" />' % image.url
        else:
            return u'Esta listing no contiene imagenes'

    imagen_miniatura.short_description = "Imagen"
    imagen_miniatura.allow_tags = True

    class Media:
        js = ('js/admin/propiedades.js',)


class OnSaleAdmin(admin.ModelAdmin):
    list_display = ('prodiedad', 'status')


class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'mobile', 'image')

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


admin.site.register(Listing, ListingAdmin)
admin.site.register(Sector)
admin.site.register(City)
admin.site.register(Agent, AgentAdmin)
admin.site.register(ListingImage, ImagenAdmin)
admin.site.register(OnSale)
admin.site.register(Attribute, AttributesAdmin)
