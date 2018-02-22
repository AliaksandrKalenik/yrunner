from rest_framework.serializers import ModelSerializer

from alesya.models import Classification


class ClassificationSerializer(ModelSerializer):

    class Meta:
        model = Classification
        fields = ("id", "name", "belong_to_class_question", "question", )
