from django.db.models import Count
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
        order_list = []
        if order.exists():
            myOrder = order[0]

            for product in myOrder.products.all():
                orderItems = {
                    'order_id': product.id,
                    'product_id': product.product.id,
                    'product_name': product.product.name,
                    'quantity': product.quantity,
                    'image': str(product.product.get_image_url),
                    'price': product.product.price,
                    'total': str(myOrder.total_price()),
                    'total_order': myOrder.orderCounter()

                }

                order_list.append(orderItems)
                # order_list.append(total)
        else:
            order_list = []

        return Response(order_list)

    def post(self, request, pk, *args, **kwargs):
        product_obj = get_object_or_404(Product, pk=pk)
        ordered_product, created = OrderedProducts.objects.get_or_create(
            customer=request.user, product=product_obj, )
        order_qs = Orders.objects.filter(customer=request.user, isPaid=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.products.filter(product__pk=product_obj.pk).exists():
                ordered_product.quantity += 1
                ordered_product.save()
                return Response({'message': 'Order updated'})
            else:
                order.products.add(ordered_product)
                return Response({'message': 'Order updated too'})
        else:
            order = Orders.objects.create(customer=request.user, )
            order.products.add(ordered_product)
            return Response({'message': ' Order created'})


class PostProduct(APIView):
    def get(self, *args, **kwargs):
        pass

    def post(self, pk, *args, **kwargs, ):
        pass
