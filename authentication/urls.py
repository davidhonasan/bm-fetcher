from django.conf.urls import url
from . import views

app_name = 'authentication'

urlpatterns = [
    url(r'^$', views.splash_page, name='main'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
]
