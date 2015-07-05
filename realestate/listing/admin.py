from django.forms import ValidationError
from django.forms.models import ModelForm
from django.contrib import admin
from sorl.thumbnail import get_thumbnail

from sorl.thumbnail.admin import AdminImageMixin

from django.utils.translation import ugettext as _

from realestate.listing.models import ListingImage, AttributeListing, Listing, Location, Agent, \
    Deal, Attribute
from realestate.listing.templatetags.extra_functions import currency
from realestate.listing.utils import validate_attribute_value, \
    copy_model_instance, import_validator


class ImageAdmin(admin.ModelAdmin):
    def friendly_title(self, obj):
        return obj.name

    def image_miniatura(self, obj):
        image = get_thumbnail(obj.image, '75x50', crop='center', quality=99)
        if image is not None:
            return '<img src="%s" />' % image.url
        return _('Image not Available')

    image_miniatura.short_description = _(u'Image')
    image_miniatura.allow_tags = True
    friendly_title.short_description = _(u'Image title')

    list_display = ('listing', 'image_miniatura', 'friendly_title', 'order')
    search_fields = ['listing', 'title']
    date_hierarchy = 'added'


def clean_attribute_value(cleaned_data):
    value = cleaned_data['value']
    attribute = cleaned_data['attribute']
    obj = cleaned_data['listing']
    success, valid_value, error_message = validate_attribute_value(attribute,
                                                                   value, obj)

    if not success:
        raise ValidationError(error_message)
    return valid_value


class ImageListingInline(AdminImageMixin, admin.TabularInline):
    model = ListingImage


class AttributeListingInlineForm(ModelForm):
    def clean_value(self):
        return clean_attribute_value(self.cleaned_data)


class AttributeListingInline(admin.TabularInline):
    model = AttributeListing
    form = AttributeListingInlineForm


class ListingAdmin(admin.ModelAdmin):
    change_form_template = "admin/realestate/listing/change_form.html"
    fieldsets = [
        (_(u'Listing Description'),
         {
             'fields': [
                 'title', 'description', 'price', ('baths', 'beds', 'size'),
                 'location', 'type', 'offer', 'active', 'featured',
             ]
         }
         ),
        (_('Contact Info'),
         {
             'fields': [
                 'agent', 'contact', 'notes', 'coords',
             ]
         }
         )
    ]

    inlines = [AttributeListingInline, ImageListingInline, ]

    list_display = (
        'id', 'title', 'slug', 'currency_price', 'active', 'type', 'location',
        'agent', 'created_at', 'featured', 'thumb_nail'
    )

    actions = ['duplicate_listing', ]

    def currency_price(self, listing):
        return currency(listing.price)

    currency_price.short_description = _(u'Price')

    list_display_links = ('id', 'title')
    search_fields = ['title', 'location']
    list_filter = ['created_at', 'agent', 'title', 'active', ]
    date_hierarchy = 'created_at'

    def thumb_nail(self, obj):
        imageobj = obj.main_image
        if imageobj:
            image = get_thumbnail(imageobj.image, '75x50', quality=99)
            if image is not None:
                return '<img src="%s" />' % image.url
        return _(u'No image')

    thumb_nail.short_description = _(u'Image')
    thumb_nail.allow_tags = True

    def duplicate_listing(self, request, queryset):
        for listing in queryset:
            new_listing = copy_model_instance(listing)
            new_listing.save()
            for attr in listing.attributelisting_set.all():
                new_attr = copy_model_instance(attr)
                new_attr.listing = new_listing
                new_attr.save()
            for image in listing.images.all():
                new_image = copy_model_instance(image)
                new_image.listing = new_listing
                new_image.save()

    class Media:
        js = ('js/admin/propiedades.js',)


class DealsAdmin(admin.ModelAdmin):
    list_display = ('listing', 'active', 'price', 'start_date', 'end_date')


class AgentAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'mobile', 'photo',)

    def photo(self, obj):
        imageobj = obj.image
        if imageobj:
            image = get_thumbnail(imageobj, '133x100', quality=99)
            return '<img src="%s" />' % image.url
        else:
            return _(u'Please, add an image')

    photo.short_description = _(u'Image')
    photo.allow_tags = True


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


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'location_type')


admin.site.register(Listing, ListingAdmin)
admin.site.register(ListingImage, ImageAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Deal, DealsAdmin)
admin.site.register(Attribute, AttributesAdmin)
