from rest_framework.serializers import ModelSerializer
from rest_framework_bulk.drf3.serializers import BulkSerializerMixin
from alesya.models import Tag
from library_fixes.bulk_serializer import AdaptedBulkListSerializer


class TagSerializer(BulkSerializerMixin, ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'entity', )
        list_serializer_class = AdaptedBulkListSerializer
