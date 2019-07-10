from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views



urlpatterns = [

    url(r'^detail/(?P<pk>\d+)/$', views.DetailsView.as_view()),
    url(r'^saveHouse/$', views.saveHouseView.as_view()),

]
