
from django.contrib import admin

from . import models


class TempProbeChangeAdmin(admin.ModelAdmin):
    
    list_display = ('pk', 'datetime_changed', 'enviro', 'measurement_frequency', 'temp_ideal')


admin.site.register(
    [
        models.RaspPi,
        models.RaspPiChannel,
        models.TempProbe,
        models.RelayController,
        models.Enviro,
        models.TempRecord
    ],
    admin.ModelAdmin
)
admin.site.register(models.TempProbeChange, TempProbeChangeAdmin)
