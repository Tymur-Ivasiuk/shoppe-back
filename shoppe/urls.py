from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework import routers

from shop.views import *
from shop.view_api import *
from shoppe import settings

router = routers.SimpleRouter()
router.register(r'products', ProductAPI)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),

    # api
    path('api/v1/', include(router.urls)),
    path('api/v1/orders/', OrderListAPI.as_view()),
    path('api/v1/orders/<int:pk>/', OrderDetailAPI.as_view()),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = pageNotFound
