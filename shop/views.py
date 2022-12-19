from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView

from .filters import ProductFilter
from .forms import *
from .models import *

class HomePage(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home page'
        return context

    def get_queryset(self):
        return Product.objects.all().prefetch_related('photo_set').order_by('-time_create')[:5]


class Shop(ListView):
    model = Product
    template_name = 'shop/shop.html'
    context_object_name = 'products_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop'
        context['form'] = self.filterset.form
        context['form_select'] = [(x.id, x.name) for x in Category.objects.all()]
        return context

    def get_queryset(self):
        queryset = Product.objects.all().prefetch_related(
            Prefetch('photo_set', queryset=Photo.objects.filter(index=1))
        ).order_by('-time_create')
        if self.request.GET.get('order-by'):
            queryset = queryset.order_by(self.request.GET.get('order-by'))

        self.filterset = ProductFilter(self.request.GET, queryset=queryset)

        return self.filterset.qs

    # def get(self, request):
    #     print(request.GET)
    #
    #     return render(request, self.template_name, )




class ProductView(DetailView):
    model = Product
    template_name = 'shop/product.html'
    pk_url_kwarg = 'product_id'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['product']
        context['photos'] = Photo.objects.filter(product_id=self.kwargs['product_id'])

        return context




def pageNotFound(request, exception):
    return render(request, 'shop/error.html', {'title': 'Страница не найдена'})
