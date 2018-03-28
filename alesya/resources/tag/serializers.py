from rest_framework.serializers import ModelSerializer
from rest_framework_bulk.drf3.serializers import BulkSerializerMixin
from alesya.models import ClassifierTag
from library_fixes.bulk_serializer import AdaptedBulkListSerializer


class ClassifierTagSerializer(BulkSerializerMixin, ModelSerializer):

    class Meta:
        model = ClassifierTag
        fields = ('id', 'name', 'classifier', )
        list_serializer_class = AdaptedBulkListSerializer
