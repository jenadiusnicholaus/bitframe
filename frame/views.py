
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from frame.models import Frame
from frame.serializers import FrameSerializers, FrameByAuthSerializer


class FrameListView(viewsets.ReadOnlyModelViewSet):
    model = Frame
    permission_classes = [permissions.AllowAny]
    serializer_class = FrameByAuthSerializer

    def get_queryset(self):
        frame = Frame.objects.filter()
        return frame


class RegisterFrame(generics.ListCreateAPIView):
    queryset = Frame.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'head', 'post', ]
    serializer_class = FrameSerializers
    authentication_class = JWTAuthentication

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        print(serializer)
        return super(RegisterFrame, self).perform_create(serializer)


class GetFrameByAuthView(viewsets.ModelViewSet):
    model = Frame
    serializer_class = FrameByAuthSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = JWTAuthentication

    def get_queryset(self):

        return Frame.objects.filter(owner=self.request.user)


class GetMultipleQuerrySet(ListAPIView):
    pagination_class = None
    queryset = Frame.objects.all()
    slice_size = 10
    serializer_class = FrameSerializers

    def get_object(self):
        try:
            obj = self.request.user
            return obj
        except ObjectDoesNotExist as e:
            raise e

    def get_queryset(self):
        frame = self.queryset.filter(owner=self.get_object())[:self.slice_size]
        product = self.queryset.values().annotate(count_opinions=Count('categories_id'))
        # pro = product[0].count_opinions
        # print(pro)
        return product
