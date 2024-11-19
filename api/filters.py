from django_filters.rest_framework import FilterSet

from storeapp.models import Product


class ProductFilterSet(FilterSet):
    class Meta:
        model = Product
        fields = {
            "category": ["exact"],
            "top_deal": ["exact"],
            "old_price": ["lt", "gt"],
        }
