from rest_framework.serializers import Serializer, DateField, \
    PrimaryKeyRelatedField, CurrentUserDefault, DecimalField, IntegerField


class WeekReport(object):
    FIELDS = [
        'week_start_date',
        'week_end_date',
        'average_speed',
        'average_time',
        'total_distance',
        'user',
    ]

    def __init__(self, **kwargs):
        for field in self.FIELDS:
            setattr(self, field, kwargs.get(field, None))


class RaceReportSerializer(Serializer):

    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    start_date = DateField(write_only=True)
    end_date = DateField(write_only=True)
    week_start_date = DateField(read_only=True)
    week_end_date = DateField(read_only=True)
    average_speed = DecimalField(read_only=True, max_digits=28, decimal_places=2)
    average_time = DecimalField(read_only=True, max_digits=28, decimal_places=2)
    total_distance = IntegerField(read_only=True)

    def create(self, validated_data):
        result = WeekReport(id=None, **validated_data)
        return result
