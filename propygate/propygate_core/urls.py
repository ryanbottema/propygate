
from django.conf.urls import include, url
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy

import views

urlpatterns = [
	
	url(r'^login$', login, name="login"),
    url(r'^logout$', logout, {'next_page': reverse_lazy("login")}, name="logout"),
]