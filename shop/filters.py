import django_filters
from django import forms
from django.db.models import Max
from django_filters.widgets import BooleanWidget

from .models import *

class ProductFilter(django_filters.FilterSet):
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None, max_value=300):
        super(ProductFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        self.filters['price_max'] = django_filters.NumberFilter(
                field_name='price',
                lookup_expr='lte',
                widget=forms.NumberInput(
                    attrs={'type': 'range', 'name': 'price-max', 'min': '0', 'max': max_value, 'value': max_value, 'id': 'slider-2',
                           'oninput': 'slideTwo()', 'step': ''})
            )
        self.filters['price_min'] = django_filters.NumberFilter(
            field_name='price',
            lookup_expr='gte',
            widget=forms.NumberInput(
                attrs={'type': 'range', 'name': 'price-min', 'min': '0', 'max': max_value, 'value': '0',
                       'id': 'slider-1', 'oninput': 'slideOne()', 'step': ''})
        )


    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='istartswith',
        widget=forms.TextInput(attrs={'placeholder': 'Search...'})
    )
    category = django_filters.CharFilter(
        field_name='category',
        lookup_expr='exact',
        widget=forms.TextInput(attrs={'name': 'category', 'value': '', })
    )
    in_stock = django_filters.NumberFilter(
        field_name='quantity',
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={'name': 'in_stock', 'value': '0', 'step': '', 'style': 'display: none;'})
    )
    on_sale = django_filters.NumberFilter(
        field_name='sale',
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={'name': 'on_sale', 'value': '0', 'step': '', 'style': 'display: none;'})
    )

    class Meta:
        model = Product
        fields = [
            'title',
            'quantity',
        ]