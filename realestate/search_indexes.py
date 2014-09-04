import datetime
from haystack import indexes
from realestate.listing.models import Listing


class ListingIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', )
    slug = indexes.CharField(model_attr='slug')
    baths = indexes.IntegerField(model_attr='baths')
    beds = indexes.IntegerField(model_attr='beds')
    date_updated = indexes.DateTimeField(model_attr='last_modified')

    def get_model(self):
        return Listing

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(last_modified__lte=datetime.datetime.now())

    def get_updated_field(self):
        return 'last_modified'