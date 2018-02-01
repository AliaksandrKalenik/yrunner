from rest_framework.fields import CurrentUserDefault
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from race.models import Race


class RaceSerializer(ModelSerializer):

    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

    class Meta:
        model = Race
        fields = ("id", "user", "distance", "time", "date", )
