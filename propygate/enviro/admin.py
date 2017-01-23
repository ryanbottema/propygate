
from django.contrib import admin

from . import models


admin.site.register(
    [
        models.RaspPi,
        models.RaspPiChannel,
        models.TempProbe,
        models.RelayController,
        models.Enviro,
        models.TempProbeChange,
        models.TempRecord
    ],
    admin.ModelAdmin
)
