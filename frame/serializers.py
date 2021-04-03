from rest_framework import serializers

from authentication.models import User
from frame.models import Frame


class FrameSerializers(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = ('owner', 'name', 'capacity', 'frame_type', 'price', 'duration')
        read_only_fields = ('owner',)

        def create(self, validated_data):
            return Frame.objects.create(**validated_data)


class FrameByAuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = Frame
        fields = "__all__"
