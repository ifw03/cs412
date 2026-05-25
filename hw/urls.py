from django.urls import path
from django.conf import settings
from . import views

#URL patterns specific
urlpatterns = [
    path(r'', views.home, name="home"),
]