from rest_framework.serializers import ModelSerializer

from alesya.models import Tag


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'classification', )
