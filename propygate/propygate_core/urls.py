
from django.urls import path
from django.contrib.auth.views import auth_login, auth_logout
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, logout
from django.urls import reverse_lazy

from . import views

urlpatterns = [

    path('', views.Home.as_view(), name="home"),
    path('getchartdata', views.GetChartData.as_view(), name='get_chart_data'),
    path('togglerelay', views.ToggleRelay.as_view(), name='toggle_relay'),
    path('login', auth_views.LoginView.as_view(), name="login"),
    path('logout', auth_views.LogoutView.as_view(), {'next_page': reverse_lazy("login")}, name="logout"),
]
