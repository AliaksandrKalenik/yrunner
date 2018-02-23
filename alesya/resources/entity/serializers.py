from rest_framework.serializers import ModelSerializer

from alesya.models import Entity


class EntitySerializer(ModelSerializer):

    class Meta:
        model = Entity
        fields = ("id", "name", "belong_to_class_question", "question", )
