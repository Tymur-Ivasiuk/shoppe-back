from django.conf.urls.static import static
from django.urls import path

from shoppe import settings
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('shop/', Shop.as_view(), name='shop'),
    path('product/<int:product_id>', ProductView.as_view(), name='product_page'),
    path('privacy-policy/', TermsOfServives.as_view(), name='privacy'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('account/', AccountView.as_view(), name='account'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/<int:order_id>/', OrderView.as_view(), name='order'),

    #favorites
    path('favorites/<id>/add/', add_to_favorites, name='add_fav'),
    path('favorites/<id>/remove/', remove_from_favorites, name='remove_fav'),

    #cart
    path('cart-options/<id>/add', add_to_cart, name='add_cart'),
    path('cart-options/<id>/remove', remove_from_cart, name='remove_cart'),
    path('cart-options/clear', clear_cart, name='clear_cart'),
    path('cart-options/sale', sale_cart, name='sale_cart'),

    #order
    path('create-order/', create_order, name='create_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

