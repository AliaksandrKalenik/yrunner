import os
from django.db import models
from django.conf import settings


WEIGHTS_PATH = os.path.join(settings.BASE_DIR, 'templates', 'nt_weights')


class TrainModelRequest(models.Model):

    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
    record_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Record created",
    )
    record_modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Record modified",
    )
    train_data_url = models.URLField(
        verbose_name="Train data URL"
    )
    status = models.CharField(
        choices=(
            (PENDING, PENDING),
            (IN_PROGRESS, IN_PROGRESS),
            (COMPLETED, COMPLETED),
            (FAILED, FAILED),
        ),
        default=PENDING,
        max_length=100,
    )
    model_path = models.FilePathField(
        verbose_name="Model path",
        default=WEIGHTS_PATH
    )
    log = models.TextField(
        verbose_name="Log",
        default="",
    )


class StyleTransferRequest(models.Model):

    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
    record_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Record created",
    )
    record_modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Record modified",
    )
    text = models.TextField(
        verbose_name="Input your text"
    )
    status = models.CharField(
        choices=(
            (PENDING, PENDING),
            (IN_PROGRESS, IN_PROGRESS),
            (COMPLETED, COMPLETED),
            (FAILED, FAILED),
        ),
        default=PENDING,
        max_length=100,
    )
    result_text = models.TextField(
        verbose_name="Result text"
    )
    log = models.TextField(
        verbose_name="Log",
        default="",
    )
