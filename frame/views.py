from django.shortcuts import render
from rest_framework import generics, permissions, status

# Create your views here.
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from frame.models import Frame
from frame.serializers import FrameSerializers


class RegisterFrame(generics.ListCreateAPIView):
    queryset = Frame.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'head', 'post']
    serializer_class = FrameSerializers
    authentication_class = JSONWebTokenAuthentication

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        print(serializer)
        return super(RegisterFrame, self).perform_create(serializer)
