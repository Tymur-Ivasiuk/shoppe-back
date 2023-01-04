from rest_framework.decorators import action
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from shop.models import *
from shop.permissions import IsOwnerOrAdmin
from shop.serializers import *


class ProductAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        categories = Category.objects.get(pk=pk)
        return Response({'cats': categories.name})

    @action(methods=['get'], detail=False)
    def categories(self, request):
        categories = Category.objects.all()
        return Response({'categories': [c.name for c in categories]})


class OrderListAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser,)


class OrderDetailAPI(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        return self.retrieve(request, *args, **kwargs)
