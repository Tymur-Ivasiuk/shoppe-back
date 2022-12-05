from django.conf.urls.static import static
from django.urls import path

from shoppe import settings
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('all-products/', all_products, name='all_products'),
    path('product/<int:product_id>', product, name='product_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = pageNotFound