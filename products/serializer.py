from rest_framework import serializers

from frame.models import Frame
from products.models import Product, Categories


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = '__all__'


class ProductCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
