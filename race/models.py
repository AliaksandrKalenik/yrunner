from django.contrib.auth import get_user_model
from django.db import models


USER_MODEL = get_user_model()


class Race(models.Model):

    user = models.ForeignKey(
        USER_MODEL, related_name='races', verbose_name="User",
    )
    distance = models.IntegerField(verbose_name="Distance(meters)")
    time = models.TimeField(verbose_name="Race time")
    date = models.DateField(verbose_name="Race date")
