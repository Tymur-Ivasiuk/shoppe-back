from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch, Avg
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
        return Product.objects.all().prefetch_related('photo_set').order_by('-time_create')[:6]


class Shop(ListView):
    model = Product
    template_name = 'shop/shop.html'
    context_object_name = 'products_list'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop'
        context['form'] = self.filterset.form
        context['form_select'] = {str(x.id): x.name for x in Category.objects.all()}
        context['ordering'] = {
            '-time_create': 'First new',
            'title': 'A -> Z',
            '-title': 'Z -> A',
            'sku': 'SKU',
            'price': 'Price: Low-High',
            '-price': 'Price: High-Low'
        }
        if self.request.GET:
            print(self.request.GET)
        context['get_items'] = self.request.GET
        return context

    def get_queryset(self):
        queryset = Product.objects.all().prefetch_related(
            Prefetch('photo_set', queryset=Photo.objects.filter(index=1))
        ).order_by('-time_create')
        if self.request.GET.get('order_by'):
            queryset = queryset.order_by(self.request.GET.get('order_by'))

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
        stars_set = Review.objects.filter(product=self.kwargs['product_id']).aggregate(Avg('star_rating')).get('star_rating__avg')
        context['avg_star'] = round(stars_set) if stars_set else 0

        context['similar'] = Product.objects.filter(category=context['object'].category).exclude(id=self.kwargs['product_id']).prefetch_related(
            Prefetch('photo_set', queryset=Photo.objects.filter(index=1))
        ).order_by('-time_create')[:3]

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
        context['orders'] = context['user'].order_set.all().order_by('-time_create')
        context['user_form'] = UpdateUserForm(instance=self.request.user)

        liked_id = self.request.session.get('favorites')
        if liked_id:
            liked_id = [int(x) for x in liked_id]
            context['liked'] = Product.objects.filter(id__in=liked_id)
        else:
            context['liked'] = False

        return context

    def post(self, request):
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            print('DEGENERAT')

        return redirect(request.path)



class CartView(TemplateView):
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cart'
        try:
            cart_id = self.request.session.get('cart').get('items')
        except:
            cart_id = False

        if cart_id:
            cart_id = [int(x) for x in cart_id]
            context['items'] = Product.objects.filter(id__in=cart_id).prefetch_related(
                Prefetch('photo_set', queryset=Photo.objects.filter(index=1))
            )
        else:
            context['items'] = False

        return context



class CheckoutView(TemplateView):
    template_name = 'shop/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Checkout'
        context['order_form'] = OrderForm()

        items = [int(x) for x in self.request.session.get('cart').get('items').keys()]
        context['items'] = Product.objects.filter(id__in=items)

        return context


def create_order(request):
    if request.method == 'POST':
        shipping_price = 10

        sale_id = request.session['cart']['sale'].get('id') if request.session['cart'].get('sale') else None
        sale = Coupon.objects.get(id=sale_id) if sale_id else None

        user_id = request.user.id if request.user.is_authenticated else None
        user = User.objects.get(id=user_id) if user_id else None

        order = Order.objects.create(
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            company_name = request.POST.get('company_name'),
            country = request.POST.get('country'),
            town = request.POST.get('town'),
            street = request.POST.get('street'),
            postcode = request.POST.get('postcode'),
            phone = request.POST.get('phone'),
            email = request.POST.get('email'),
            order_notes = request.POST.get('order_notes'),

            sale = sale,
            user = user,
            shipping_price = shipping_price
        )
        product_list = Product.objects.filter(id__in=[int(x) for x in request.session['cart']['items'].keys()])
        for i in product_list:
            OrderList.objects.create(
                order=order,
                product=i,
                quantity=request.session['cart']['items'][str(i.id)]['quantity'],
                price=request.session['cart']['items'][str(i.id)]['price']
            )

        response = redirect('order', order_id=order.id)

        if not request.user.is_authenticated:
            if not request.COOKIES.get('orders_can_view'):
                response.set_cookie('orders_can_view', [order.id])
            else:
                list_orders = [int(x) for x in request.COOKIES.get('orders_can_view').strip('][').split(',')]
                list_orders.append(order.id)
                response.set_cookie('orders_can_view', list_orders)

        del request.session['cart']
        request.session.modified = True

    return response


class OrderView(DetailView):
    template_name = 'shop/order.html'
    model = Order
    pk_url_kwarg = 'order_id'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Order - {context["order"]}'


        context['can_view'] = False
        print(self.request.COOKIES)

        if self.request.COOKIES.get('orders_can_view'):
            list_orders = [int(x) for x in self.request.COOKIES.get('orders_can_view').strip('][').split(',')]
            print(list_orders, context['order'].id)
            if context['order'].id in list_orders:
                context['can_view'] = True

        if self.request.user.is_authenticated:
            print(self.request.user.id)
            if context['order'].user and self.request.user.id == context['order'].user.id:
                context['can_view'] = True

        print(context)
        return context





def logout_user(request):
    logout(request)
    return redirect('home')



def add_to_favorites(request, id):
    if request.method == 'POST':
        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
            request.session['favorites'] = list(request.session['favorites'])

        if not id in request.session['favorites']:
            request.session['favorites'].append(id)
            request.session.modified = True

    return redirect(request.POST.get('url_from'))


def remove_from_favorites(request, id):
    if request.method == 'POST':
        while str(id) in request.session['favorites']:
            request.session['favorites'].remove(str(id))
            request.session.modified = True

        if not request.session['favorites']:
            del request.session['favorites']
    return redirect(request.POST.get('url_from'))





#cart
def add_to_cart(request, id):
    if request.method == 'POST':
        print(request.POST)
        if not request.session.get('cart'):
            request.session['cart'] = dict()
            request.session['cart']['items'] = dict()

        else:
            request.session['cart']['items'] = dict(request.session['cart'].get('items'))

        if request.session['cart']['items'].get(id):
            if int(request.POST.get('quantity')) != 0:
                request.session['cart']['items'][id]['quantity'] = int(request.POST.get('quantity'))
            else:
                del request.session['cart']['items'][id]
        else:
            data = {
                'quantity': int(request.POST.get('quantity')),
                'price': float(request.POST.get('price').replace(',', '.')),
            }
            request.session['cart']['items'][id] = data

        request.session.modified = True
        return redirect(request.POST.get('url_from'))



def remove_from_cart(request, id):
    if request.method == 'POST':
        del request.session['cart']['items'][id]
        request.session.modified = True
    return redirect(request.POST.get('url_from'))

def clear_cart(request):
    if request.method == 'POST':
        del request.session['cart']
    return redirect(request.POST.get('url_from'))

def sale_cart(request):
    if request.method == 'POST':
        try:
            coupon = Coupon.objects.get(code=request.POST.get('sale_code'))
        except:
            coupon = False

        if coupon:
            print(coupon.order_set.count())
            if coupon.order_set.count() < coupon.max_uses:
                data = {
                    'id': coupon.id,
                    'code': coupon.code,
                    'sale': coupon.sale_percent
                }
                request.session['cart']['sale'] = data
            else:
                request.session['cart']['sale'] = 'max'
        else:
            request.session['cart']['sale'] = 'nothing'
        request.session.modified = True
    return redirect(request.POST.get('url_from'))

def pageNotFound(request, exception):
    return render(request, 'shop/error.html', {'title': 'Страница не найдена'})
