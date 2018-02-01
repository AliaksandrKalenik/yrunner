from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models


USER_MODEL = get_user_model()


class Image(models.Model):

    optimized = models.ImageField(
        upload_to="images/",
        null=True,
        blank=True,
        max_length=5000,
    )
    origin = models.ImageField(
        upload_to="images/",
        max_length=5000,
    )
