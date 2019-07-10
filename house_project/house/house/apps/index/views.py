from django.shortcuts import render

# Create your views here.
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from index.serializers import IndexSerialzer
from info.models import House, Container
from house.utils.pagnations import StandardResultsSetPagination


class IndexInfoView(ListAPIView):
    filter_backends = [OrderingFilter]
    ordering = ['unitPrice', 'area', 'price','id','time']
    pagination_class = StandardResultsSetPagination
    serializer_class = IndexSerialzer
    queryset = House.objects.all()
    # def get(self,request):
    #     try:
    #         houses = House.objects.all()
    #     except:
    #         return Response({"error":'错误'})
    #     content=[]
    #     for house in houses:
    #         data_dict={
    #             'id':house.id,
    #             'title':house.title,
    #             'vide':house.vide,
    #             'price':house.price,
    #             'souce':house.source
    #
    #         }
    #
    #         content.append(data_dict)
    #     return Response(data=content)
class  IndexSelectView(ListAPIView):
    filter_backends = [OrderingFilter]
    ordering = ['unitPrice', 'area', 'price','id','time']
    pagination_class = StandardResultsSetPagination#分页这个就是，django框架封装好的
    serializer_class = IndexSerialzer

    def get_queryset(self):
        data = self.request.query_params.dict()['selectData']
        data_list = data.split(',')
        id_list = []
        for data in data_list:
            containers = Container.objects.filter(content__contains=data)
            for container in containers:
                id_list.append(container.id)
        id_list=list(set(id_list))
        self.queryset = House.objects.filter(Container_id__in=id_list).all()

        return self.queryset