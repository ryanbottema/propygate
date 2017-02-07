
from django.contrib import admin

from . import models


class IdealsAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime_changed', 'enviro', 'temp_ideal')


class TempRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'enviro', 'temperature', 'datetime_recorded')

class RelayControllerToggleAdmin(admin.ModelAdmin):
    list_display = ('id', 'relay_controller', 'is_on', 'datetime_toggled')


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
admin.site.register(models.RelayControllerToggle, RelayControllerToggleAdmin)
admin.site.register(models.TempRecord, TempRecordAdmin)
admin.site.register(models.Ideals, IdealsAdmin)
