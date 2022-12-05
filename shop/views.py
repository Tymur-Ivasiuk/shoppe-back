from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from .models import *


def index(request):
    products = Product.objects.all().prefetch_related('photo_set').order_by('-time_create')[:5]
    ctx = {
        'title': 'ГЛАВНАЯ СТРАНИЦА',
        'products': products,
    }
    return render(request, 'shop/index.html', ctx)

def all_products(request):
    return HttpResponse('<h1>Все продукти</h1>')

def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    photos = get_list_or_404(Photo, product_id=product_id)
    return render(request, 'shop/product.html', {'title': 'Product info', 'product': product, 'photos': photos})




def pageNotFound(request, exception):
    return render(request, 'shop/error.html', {'title': 'Страница не найдена'})
