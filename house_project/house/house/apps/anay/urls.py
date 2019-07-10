from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [

    url(r'^address_qu_count/$', views.addressQuCount.as_view()),
    url(r'^house_type_count/$', views.houseTypeCount.as_view()),
    url(r'^area_price/$', views.areaPrice.as_view()),
    url(r'^house_type_vide/$', views.houseTypeVide.as_view()),
    url(r'^address_qu_avg/$', views.addressQuAvg.as_view()),
    url(r'^address_wu_num/$', views.addressWuNum.as_view()),
    url(r'^address_wu_vide/$', views.addressWuVide.as_view()),
    url(r'^house_area/$', views.houseArea.as_view()),

]