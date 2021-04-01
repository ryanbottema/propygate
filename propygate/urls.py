
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path

urlpatterns = [
	path('', RedirectView.as_view(pattern_name='home', permanent=False)),
	path('admin/', admin.site.urls),
	path('propygate/', include('propygate.propygate_core.urls')),
	# path('', include('django_registration.backends.one_step.urls')),
]
