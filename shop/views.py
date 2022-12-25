from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView

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


class ProductView(DetailView):
    model = Product
    template_name = 'shop/product.html'
    pk_url_kwarg = 'product_id'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['product']

        context['review_form'] = ReviewForm()

        context['similar'] = Product.objects.filter(category=context['object'].category).exclude(id=self.kwargs['product_id']).prefetch_related(
            Prefetch('photo_set', queryset=Photo.objects.filter(index=1))
        ).order_by('-time_create')

        return context

    def post(self, request, product_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = Product.objects.get(id=product_id)
            if request.user.is_authenticated:
                form.user = request.user
                form.name = f'{request.user.first_name} {request.user.last_name}'
            form.save()
        return redirect('product_page', product_id)


class TermsOfServives(TemplateView):
    template_name = 'shop/privacy.html'



# user
class RegisterUser(CreateView):
    template_name = 'shop/register.html'
    success_url = reverse_lazy('login')
    form_class = RegisterUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'shop/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        return reverse_lazy('account')

class AccountView(TemplateView):
    template_name = 'shop/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Account'
        context['user'] = User.objects.get(username=self.request.user)




def logout_user(request):
    logout(request)
    return redirect('home')

def pageNotFound(request, exception):
    return render(request, 'shop/error.html', {'title': 'Страница не найдена'})
