import os

from django.contrib import admin

# Register your models here.
from rest_framework.status import HTTP_404_NOT_FOUND

from text_style_transfer.models import TrainModelRequest, StyleTransferRequest, \
    WEIGHTS_PATH
from text_style_transfer.tasks import train_model, transfer_style


@admin.register(TrainModelRequest)
class TrainModelRequestAdmin(admin.ModelAdmin):

    list_display = ['id', 'status', 'model_path', 'record_created', 'record_modified', ]
    readonly_fields = ('status', 'model_path', 'log', )

    def save_model(self, request, obj, form, change):
        result = super(TrainModelRequestAdmin, self).save_model(request, obj, form, change)
        train_model.apply_async(args=(obj.id, obj.train_data_url), retry=False)
        return result


@admin.register(StyleTransferRequest)
class StyleTransferRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'record_created', 'record_modified', ]
    readonly_fields = ('status', 'log', 'result_text', )

    def save_model(self, request, obj, form, change):
        if not os.path.exists(WEIGHTS_PATH):
            return HTTP_404_NOT_FOUND("Trainded model not found. You should train model first.")
        result = super(StyleTransferRequestAdmin, self).save_model(request, obj, form, change)
        transfer_style.apply_async(args=(obj.id, obj.text), retry=False)
        return result
