import uuid
from datetime import *

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeDoneView, PasswordResetCompleteView, \
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.core.mail import EmailMessage, mail_admins
from django.db.models import Prefetch, Avg
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, FormView

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


class TermsOfServices(TemplateView):
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

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(self.request.POST)
        if form.is_valid():
            user = form.save()

            auth_token = str(uuid.uuid4())
            password_token = str(uuid.uuid4())

            profile = Profile.objects.get_or_create(user=user)
            profile[0].auth_token = auth_token
            profile[0].password_token = password_token
            profile[0].save()

            send_email_verify(user.email, auth_token)
            messages.success(request, 'An email has been sent to your email. Please verify your email address')
            return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})


def send_email_verify(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi! Paste the link to verify your account \n\nhttp://127.0.0.1:8000/verify/{token}'
    recipient_list = [email]
    msg = EmailMessage(subject, message, to=recipient_list)
    msg.send()


def verify(request, auth_token):
    try:
        profile = Profile.objects.filter(auth_token=auth_token).first()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('login')

    if profile:
        if profile.email_verify:
            messages.success(request, 'Your email has already been verified')
            return redirect('login')
        profile.email_verify = True
        profile.save()
        messages.success(request, 'Your account has been successfully verified')
    else:
        messages.error(request, 'Something went wrong')

    return redirect('login')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'shop/login.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('account')
        return super(LoginUser, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def form_valid(self, form):
        user = form.get_user()
        if user.profile.email_verify:
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Please verify your email')
            return redirect('login')

    def get_success_url(self):
        if self.request.GET.get('next'):
            return str(self.request.GET.get('next'))
        return reverse_lazy('account')


class AccountView(TemplateView):
    template_name = 'shop/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Account'
        context['user'] = User.objects.get(username=self.request.user)
        context['orders'] = context['user'].order_set.all().prefetch_related('orderlist_set').order_by('-time_create')
        context['user_form'] = UpdateUserForm(instance=self.request.user)

        if self.request.user.is_authenticated:
            liked_id = self.request.user.profile.user_json.get('liked')
        else:
            liked_id = self.request.COOKIES.get('liked')
            liked_id = [int(x) for x in liked_id.strip('][').split(',')]

        if liked_id:
            context['liked'] = Product.objects.filter(id__in=liked_id)
        else:
            context['liked'] = False

        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super(AccountView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        user_email = request.user.email
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('email') != user_email:
                profile = Profile.objects.get(user=user)

                auth_token = str(uuid.uuid4())
                send_email_verify(user.email, auth_token)
                messages.success(request, 'An email has been sent to your email. Please verify your email address')

                profile.email_verify = False
                profile.auth_token = auth_token
                profile.save()
                logout(request)

                return redirect('login')
        return redirect(request.path)


class ChangePasswordReset(PasswordResetView):
    template_name = 'shop/reset_password.html'
    form_class = ResetPasswordEmail

class ChangePasswordResetDone(PasswordResetDoneView):
    template_name = 'shop/reset_password_done.html'

class ChangePasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'shop/reset_password_confirm.html'
    form_class = SetPassword

class ChangePasswordResetComplete(PasswordResetCompleteView):
    template_name = 'shop/reset_password_complete.html'


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
                list_orders = [order.id]
            else:
                list_orders = [int(x) for x in request.COOKIES.get('orders_can_view').strip('][').split(',')]
                list_orders.append(order.id)
            max_time = datetime.now() + timedelta(days=365)
            expires = datetime.strftime(max_time, "%a, %d-%b-%Y %H:%M:%S GMT")
            response.set_cookie('orders_can_view', list_orders, expires=expires)

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

        if self.request.COOKIES.get('orders_can_view'):
            list_orders = [int(x) for x in self.request.COOKIES.get('orders_can_view').strip('][').split(',')]
            if context['order'].id in list_orders:
                context['can_view'] = True

        if self.request.user.is_authenticated:
            if context['order'].user and self.request.user.id == context['order'].user.id:
                context['can_view'] = True

        return context


class ContactView(FormView):
    template_name = 'shop/contact.html'
    form_class = ContactForm

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = f'{form.cleaned_data["message"]}\n\nUser: {form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]} \n\nEMAIL from : {form.cleaned_data["email"]}'
            mail_admins(subject=subject, message=message)
            messages.success(request, 'Your email has been sent to the site administrator. Thanks for the feedback')
        return redirect(request.path)


def logout_user(request):
    logout(request)
    return redirect('home')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def add_to_favorites(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(f'{reverse("login")}?next={request.POST.get("url_from")}')

    id = request.POST.get('id')

    if request.method == 'POST':
        profile = request.user.profile

        if profile.user_json.get('liked'):
            profile.user_json['liked'].append(id)
        else:
            profile.user_json['liked'] = [id]
        profile.save()

    # AJAX
    if is_ajax(request=request):
        return JsonResponse({'id': id})

    return redirect('product_page', product_id=id)


def remove_from_favorites(request):
    profile = request.user.profile
    id = request.POST.get('id')

    if id in profile.user_json.get('liked'):
        profile.user_json['liked'].remove(id)
        profile.save()

    # AJAX
    if is_ajax(request=request):
        return JsonResponse({'id': id})

    return redirect('product_page', product_id=id)

def favorites_api(request):
    return JsonResponse(request.user.profile.user_json, safe=False)



#cart
def add_to_cart(request):
    id = request.POST.get('id')

    if request.method == 'POST':
        if not request.session.get('cart'):
            request.session['cart'] = dict()
            request.session['cart']['items'] = dict()

        else:
            request.session['cart']['items'] = dict(request.session['cart'].get('items'))

        if request.session['cart']['items'].get(id):
            d = request.session['cart']['items'][id]['quantity'] + int(request.POST.get('quantity'))
            if d != 0:
                product_quantity = Product.objects.get(id=int(id)).quantity
                if d <= product_quantity:
                    request.session['cart']['items'][id]['quantity'] += int(request.POST.get('quantity'))
                else:
                    request.session['cart']['items'][id]['quantity'] = product_quantity
            else:
                del request.session['cart']['items'][id]
        else:
            data = {
                'quantity': int(request.POST.get('quantity')),
                'price': float(request.POST.get('price').replace(',', '.')),
            }
            request.session['cart']['items'][id] = data

        request.session.modified = True

    if is_ajax(request=request):
        data = {
            id: {
                'quantity': int(request.POST.get('quantity')),
            }
        }
        request.session.modified = True
        return JsonResponse(data)

    return redirect(request.POST.get('url_from'))


def remove_from_cart(request):
    id = request.POST.get('id')

    if request.method == 'POST':
        del request.session['cart']['items'][id]
        request.session.modified = True

    if is_ajax(request=request):
        request.session.modified = True
        return JsonResponse({'id': id})

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

def cart_json(request):
    return JsonResponse(request.session['cart'].get('items'), safe=False)


def pageNotFound(request, exception):
    return render(request, 'shop/error.html', {'title': 'Страница не найдена'})
