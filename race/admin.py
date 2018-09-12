from django.contrib import admin
from django.contrib.admin import ModelAdmin

from race.models import Race


@admin.register(Race)
class RaceAdmin(ModelAdmin):
    pass
