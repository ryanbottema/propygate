
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import TemplateView, CreateView, DetailView, View

from propygate.enviro import models as e_models


class Home(TemplateView):
    template_name = 'propygate_core/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(*args, **kwargs)
        
        context['enviros'] = e_models.Enviro.objects.all().select_related('light', 'heater', 'temp_probe', 'temp_probe_change_current')
        return context

