
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, DetailView, View

from . import models


class Home(TemplateView):
    template_name = 'propygate_core/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        
        context['enviros'] = models.Enviro.objects.all().select_related('light', 'heater', 'temp_probe')
        return context


class GetChartData(View):

    def get(self, *args, **kwargs):

        enviros = models.Enviro.objects.all()
        enviros_data = []

        for env in enviros:

            if env.temp_probe:
                ideals = models.Ideals.objects.filter(
                    enviro=env, datetime_changed__gte=timezone.now() - timezone.timedelta(hours=24)
                )
                ideals_data = []
                for ideal in ideals:
                    ideals_data.append({
                        'datetime_changed': ideal.datetime_changed,
                        'enviro_id': ideal.enviro.id,
                        'temp_ideal': ideal.temp_ideal,
                        'temp_low_low': ideal.temp_low_low,
                        'temp_low': ideal.temp_low,
                        'temp_high': ideal.temp_high,
                        'temp_high_high': ideal.temp_high_high
                    })

                temp_records = models.TempRecord.objects.filter(
                    enviro=env, datetime_recorded__gte=timezone.now() - timezone.timedelta(hours=24)
                )
                temp_data = []
                for tr in temp_records:
                    temp_data.append({
                        'datetime_recorded': tr.datetime_recorded,
                        'temperature': tr.temperature,
                        'enviro_id': tr.enviro_id
                    })
            else:
                temp_data = False
                ideals_data = False

            if env.light:
                light_toggles = models.RelayControllerToggle.objects.filter(
                    relay_controller=env.light, datetime_toggled__gte=timezone.now() - timezone.timedelta(hours=24)
                )
                light_data = []
                for rt in light_toggles:
                    light_data.append({
                        'datetime_toggled': rt.datetime_toggled,
                        'is_on': rt.is_on,
                        'enviro_id': rt.enviro_id
                    })
            else:
                light_data = False

            if env.heater:
                heater_toggles = models.RelayControllerToggle.objects.filter(
                    relay_controller=env.heater, datetime_toggled__gte=timezone.now() - timezone.timedelta(hours=24)
                )
                heater_data = []
                for rt in heater_toggles:
                    heater_data.append({
                        'datetime_toggled': rt.datetime_toggled,
                        'is_on': rt.is_on,
                        'enviro_id': rt.enviro_id
                    })
            else:
                heater_data = False

            enviros_data.append({
                'id': env.id,
                'ideals': ideals_data,
                'temp_data': temp_data,
                'light_data': light_data,
                'heater_data': heater_data

            })

        return JsonResponse(enviros_data, safe=False)


class UpdateChartData(View):

    def get(self, *args, **kwargs):

        return JsonResponse({
            '': None,
        })
