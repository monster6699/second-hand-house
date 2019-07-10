
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views



urlpatterns = [

    url(r'^oauth/qq/authorization/$', views.OuthQQView.as_view()),
    url(r'^oauth/qq/user/$', views.QQUserView.as_view()),

]


