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
    path('account/', AccountView.as_view(),name='account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

