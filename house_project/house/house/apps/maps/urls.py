from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views



urlpatterns = [

    url(r'^anayly/$', views.StaticAsansy.as_view()),

]

