import datetime
from haystack import indexes
from realestate.listing.models import Listing
from sorl.thumbnail import get_thumbnail


class ListingIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', )
    description = indexes.CharField(model_attr='description', )
    slug = indexes.CharField(model_attr='slug')
    price = indexes.FloatField(null=True, faceted=True)
    currency = indexes.CharField(null=True, faceted=True)
    type = indexes.CharField(model_attr='type', faceted=True)
    offer = indexes.CharField(model_attr='offer', faceted=True)
    baths = indexes.IntegerField(model_attr='baths', faceted=True)
    beds = indexes.IntegerField(model_attr='beds', faceted=True)
    location = indexes.CharField(model_attr='location', null=True, faceted=True)
    featured = indexes.BooleanField(model_attr='featured', faceted=True)
    coords = indexes.CharField(model_attr='coords')
    size = indexes.FloatField(model_attr='size', faceted=True)
    agent = indexes.CharField(model_attr='agent', faceted=True)
    image = indexes.CharField(null=True)
    absolute_url = indexes.CharField(null=True)
    date_updated = indexes.DateTimeField(model_attr='last_modified')

    def get_model(self):
        return Listing

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(last_modified__lte=datetime.datetime.now())

    def get_updated_field(self):
        return 'last_modified'

    def prepare_price(self, listing):
        return listing.price.amount

    def prepare_currency(self, listing):
        return '%s' % listing.price.currency

    def prepare_location(self, listing):
        if listing.location is not None:
            return '%s' % listing.location
        return ""

    def prepare_agent(self, listing):
        if listing.agent is not None:
            return '%s' % listing.agent
        return ""

    def prepare_image(self, listing):
        try:
            return get_thumbnail(listing.main_image.image, '640x480', crop='center', quality=99).url
        except:
            return ''

    def prepare_absolute_url(self, listing):
        return listing.absolute_url
