
from django.contrib import admin

from . import models


class IdealsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'datetime_changed', 'enviro', 'temp_ideal')


class TempRecordAdmin(admin.ModelAdmin):
    list_display = ('pk', 'enviro', 'temperature', 'datetime_recorded')


admin.site.register(
    [
        models.RaspPi,
        models.RaspPiChannel,
        models.TempProbe,
        models.RelayController,
        models.Enviro,
    ],
    admin.ModelAdmin
)
admin.site.register(models.TempRecord, TempRecordAdmin)
admin.site.register(models.Ideals, IdealsAdmin)
