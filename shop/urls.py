from django.conf.urls.static import static
from django.urls import path

from shoppe import settings
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('shop/', Shop.as_view(), name='shop'),
    path('product/<int:product_id>', ProductView.as_view(), name='product_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

