
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.utils import timezone
from django.utils.dateformat import format
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

        num_records = len(models.TempRecord.objects.all()) + len(models.RelayControllerToggle.objects.all())
        if int(self.request.GET.get('num_records')) == num_records:
            return JsonResponse({'changed': False, 'num_records': num_records}, safe=False)

        enviros = models.Enviro.objects.all()
        enviros_data = []

        for env in enviros:

            if env.temp_probe:
                ideals = models.Ideals.objects.filter(
                    enviro=env, datetime_changed__gte=timezone.now() - timezone.timedelta(hours=24)
                )
                if len(ideals) == 0:
                    ideals = [env.get_current_ideals()]

                ideals_data = []
                for ideal in ideals:
                    ideals_data.append({
                        'datetime_changed': timezone.localtime(ideal.datetime_changed),
                        'enviro_id': ideal.enviro.id,
                        'temp_ideal': float(ideal.temp_ideal),
                        'temp_low_low': ideal.temp_low_low,
                        'temp_low': ideal.temp_low,
                        'temp_high': ideal.temp_high,
                        'temp_high_high': ideal.temp_high_high,
                        'x': int(format(timezone.localtime(ideal.datetime_changed), 'U')) * 1000
                    })

                temp_records = models.TempRecord.objects.filter(
                    enviro=env, datetime_recorded__gte=timezone.now() - timezone.timedelta(hours=24)
                )
                temp_data = []
                for tr in temp_records:
                    temp_data.append({
                        'datetime_recorded': timezone.localtime(tr.datetime_recorded),
                        'temperature': float(tr.temperature),
                        'enviro_id': tr.enviro_id,
                        'x': int(format(timezone.localtime(tr.datetime_recorded), 'U')) * 1000
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

                    if not rt.is_on:
                        light_data.append({
                            'is_on': True,
                            'fake_toggle': True,
                            'x': int(format(timezone.localtime(rt.datetime_toggled), 'U')) * 1000 - 1
                        })
                    light_data.append({
                        'datetime_toggled': timezone.localtime(rt.datetime_toggled),
                        'is_on': rt.is_on,
                        'enviro_id': env.id,
                        'relay_controller': rt.relay_controller_id,
                        'x': int(format(rt.datetime_toggled, 'U')) * 1000
                    })

                if len(light_data) > 0 and not light_data[0]['is_on']:
                    light_data.insert(0, {
                        'x': int(format(timezone.localtime(timezone.now() - timezone.timedelta(hours=24)), 'U')) * 1000 - 1,
                        'is_on': True,
                        'fake_toggle': True
                    })
            else:
                light_data = False

            if env.heater:
                heater_toggles = models.RelayControllerToggle.objects.filter(
                    relay_controller=env.heater, datetime_toggled__gte=timezone.now() - timezone.timedelta(hours=24)
                )
                heater_data = []
                for ht in heater_toggles:
                    if not ht.is_on:
                        heater_data.append({
                            'is_on': True,
                            'fake_toggle': True,
                            'x': int(format(timezone.localtime(ht.datetime_toggled), 'U')) * 1000 - 1
                        })
                    heater_data.append({
                        'datetime_toggled': timezone.localtime(ht.datetime_toggled),
                        'is_on': ht.is_on,
                        'enviro_id': env.id,
                        'relay_controller': ht.relay_controller_id,
                        'x': int(format(timezone.localtime(ht.datetime_toggled), 'U')) * 1000
                    })
                if len(heater_data) > 0 and not heater_data[0]['is_on']:
                    heater_data.insert(0, {
                        'x': int(
                            format(timezone.localtime(timezone.now() - timezone.timedelta(hours=24)), 'U')) * 1000 - 1,
                        'is_on': True,
                        'fake_toggle': True
                    })
            else:
                heater_data = False

            enviros_data.append({
                'name': env.name,
                'id': env.id,
                'ideals': ideals_data,
                'temp_data': temp_data,
                'light_data': light_data,
                'heater_data': heater_data,
            })

        return JsonResponse({
            'enviros_data': enviros_data,
            'num_records': num_records,
            'changed': True
        }, safe=False)


class UpdateChartData(View):

    def get(self, *args, **kwargs):

        return JsonResponse({
            '': None,
        })
