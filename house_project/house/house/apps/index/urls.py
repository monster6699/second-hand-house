from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views



urlpatterns = [
    url(r'^index/$', views.IndexInfoView.as_view()),
    url(r'^select/$', views.IndexSelectView.as_view()),

]
