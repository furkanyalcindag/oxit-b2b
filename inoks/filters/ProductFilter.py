import django_filters

from inoks.models import Product

class ProductFilter(django_filters.FilterSet):
    # price = django_filters.NumericRangeFilter()

    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['price', ]
