from rest_framework import viewsets, response, status
from rest_framework import permissions
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from frame.models import Frame
from products.models import Product, Categories, Orders, OrderedProducts
from .serializer import ProductSerializer, FrameSerializer, ProductCategoriesSerializer, OrderSerializer


class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        qs = Product.objects.filter().order_by('-created_by')
        return qs


class ProductCategories(viewsets.ModelViewSet):
    queryset = Categories.objects.filter()
    serializer_class = ProductCategoriesSerializer
    permission_classes = [permissions.AllowAny, ]


class AddToShoppingCartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = JWTAuthentication

    def get(self, request, *args, **kwargs):
        order = Orders.objects.filter(customer=request.user, isPaid=False)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    def post(self, request, pk, *args, **kwargs):
        product_obj = get_object_or_404(Product, pk=pk)
        ordered_product, created = OrderedProducts.objects.get_or_create(
            customer=request.user, product=product_obj, )
        order_qs = Orders.objects.filter(customer=request.user, isPaid=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.products.filter(product__pk=product_obj.pk).exists():
                order.quantity += 1
                order.save()
                return Response({'message': 'Order updated'})
            else:
                order.products.add(ordered_product)
                return Response({'message': 'Order updated too'})
        else:
            order = Orders.objects.create(customer=request.user, )
            order.products.add(ordered_product)
            return Response({'message': ' Order created'})
