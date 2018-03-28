from rest_framework.serializers import ModelSerializer

from alesya.models import Сlassifier


class ClassifierSerializer(ModelSerializer):

    class Meta:
        model = Сlassifier
        fields = ("id", "name", "belong_to_class_question", "question", )
