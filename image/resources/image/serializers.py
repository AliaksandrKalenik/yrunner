from uuid import uuid4
from dynamic_rest.serializers import DynamicModelSerializer
from image.models import Image


class ImageSerializer(DynamicModelSerializer):

    class Meta:
        model = Image
        name = 'image'
        fields = "__all__"

    def create(self, validated_data):
        self.modify_origin_name(validated_data)
        return super(ImageSerializer, self).create(validated_data)

    def modify_origin_name(self, validated_data):
        origin = validated_data.get('origin')
        if validated_data:
            validated_data['origin'].name = "_".join([str(uuid4()), origin.name])

    def save(self, *args, **kwargs):
        self.user = self.context['request'].user
        return super(ImageSerializer, self).save(*args, **kwargs)
