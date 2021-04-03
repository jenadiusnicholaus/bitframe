from rest_framework import viewsets, response, status
from rest_framework import permissions
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from frame.models import Frame
from products.models import Product
from .serializer import ProductSerializer, FrameSerializer


class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        qs = Product.objects.filter().order_by('-created_by')
        return qs


class ProductFrame():
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        qs = Product.objects.filter().order_by('-created_by')
        return qs

