
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import TemplateView, CreateView, DetailView, View


class Home(TemplateView):
	
	template_name = 'propygate_core/home.html'
	
	def get_context_data(self, *args, **kwargs):
		context = super(Home, self).get_context_data(*args, **kwargs)
		context['VERSION'] = settings.VERSION
		context['STATIC_URL'] = settings.STATIC_URL
		context['DEBUG'] = settings.DEBUG
		return context
	
	