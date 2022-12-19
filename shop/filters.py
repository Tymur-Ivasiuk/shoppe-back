import django_filters
from django import forms
from django.db.models import Max
from django_filters.widgets import BooleanWidget

from .models import *

class ProductFilter(django_filters.FilterSet):
    max_price = str(int(Product.objects.aggregate(Max('price'))['price__max']))

    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='istartswith',
        widget=forms.TextInput(attrs={'placeholder': 'Search...'})
    )
    category = django_filters.CharFilter(
        field_name='category_id',
        lookup_expr='exact',
        widget=forms.TextInput(attrs={'name': 'category', 'value': '', })
    )
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={'type': 'range', 'name': 'price-min', 'min': '0', 'max': max_price, 'value': '0', 'id': 'slider-1', 'oninput': 'slideOne()', 'step':''})
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        widget=forms.NumberInput(
            attrs={'type': 'range', 'name': 'price-max', 'min': '0', 'max': max_price, 'value': max_price, 'id': 'slider-2',
                   'oninput': 'slideTwo()', 'step': ''})
    )
    in_stock = django_filters.NumberFilter(
        field_name='quantity',
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={'name': 'in_stock', 'value': '0', 'step': '', 'style': 'display: none;'})
    )



    class Meta:
        model = Product
        fields = [
            'title',
            #'on_sale' in future
            'quantity',
        ]