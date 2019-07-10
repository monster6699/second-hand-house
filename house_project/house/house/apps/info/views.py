from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from info.models import House, Image, HouseCharact, BaseAttr, Tag, SelecttData, Container
from info.serializers import DetailSerilazer
from users.models import Follow
import json

class DetailsView(APIView):
    def perform_authentication(self, request):
        pass
    def get(self,request,pk):
        try:
            user = request.user
        except:
            user = None
        try:
            houses =  House.objects.get(id=pk)
        except:
            Response("查询信息错误")
        data_dict={}

        data_dict['title']=houses.title
        data_dict['price'] =int(houses.price)
        data_dict['unitPrice'] =houses.unitPrice
        data_dict['url'] =houses.url
        data_dict['vide'] =houses.vide
        data_dict['focus'] =houses.focus
        data_dict['user'] = None
        if user:
            try:
                follow = Follow.objects.get(user_id=user.id,house_id=pk)
            except:
                follow=None
            if follow:
                data_dict['user'] =follow.user.id
            else:
                data_dict['user'] = None
        data_dict['houseType'] =houses.baseAttr.houseType
        data_dict['floor'] =houses.baseAttr.floor
        data_dict['area'] =houses.baseAttr.area
        data_dict['structure'] =houses.baseAttr.structure
        data_dict['inArea'] =houses.baseAttr.inArea
        data_dict['buildType'] =houses.baseAttr.buildType
        data_dict['buildHead'] =houses.baseAttr.buildHead
        data_dict['buildStruct'] =houses.baseAttr.buildStruct
        data_dict['decorate'] =houses.baseAttr.decorate
        data_dict['ladderHouPro'] =houses.baseAttr.ladderHouPro
        data_dict['heatMethod'] =houses.baseAttr.heatMethod
        data_dict['lift'] =houses.baseAttr.lift
        data_dict['period'] =houses.baseAttr.period
        data_dict['address_wu'] =houses.baseAttr.address_wu
        data_dict['address_qu'] =houses.baseAttr.address_qu
        data_dict['address_detail'] =houses.baseAttr.address_detail


        data_dict['listedTime'] =houses.tradeAttr.listedTime
        data_dict['tradeOwershid'] =houses.tradeAttr.tradeOwershid
        data_dict['lastTransationTime'] =houses.tradeAttr.lastTransationTime
        data_dict['house_use'] =houses.tradeAttr.house_use
        data_dict['house_year'] =houses.tradeAttr.house_year
        data_dict['belongTo'] =houses.tradeAttr.belongTo
        data_dict['mortgageInfo'] =houses.tradeAttr.mortgageInfo
        data_dict['roomBak'] =houses.tradeAttr.roomBak


        try:
            pk=pk
            images = Image.objects.filter(house=pk)
        except:
            return Response("查询图片错误")
        image_list=[]
        for image in images:
            image_dict={
                "name":image.name,
                'url':image.url
            }
            image_list.append(image_dict)
        data_dict['images']=image_list

        charact_list =[]

        try:
            pk=pk
            houseCharact = HouseCharact.objects.filter(house=pk)
        except:
            return Response("查询房源特色错误")
        for data in houseCharact:
            charact_dict={
                'name':data.name,
                'content':data.content
            }

            charact_list.append(charact_dict)

        data_dict['charactData'] = charact_list
        print(data_dict)

        return Response(data=data_dict)





    # serializer_class = DetailSerilazer
    # def get_queryset(self):
    #     id =  self.kwargs['pk']
    #     return House.objects.get(id=id)



class saveHouseView(APIView):
    def perform_authentication(self, request):
        pass

    def post(self, request):
        try:
            user = request.user
        except:
            user = None
        if not user:
            return Response("登陆后才能发布房源")
        houseData = request.data.get('params')['houseData']
        houseData = json.loads(houseData)
        return Response('ok')
        BaseAttr.houseType=houseData['houseType']
        BaseAttr.floor=houseData['houseNum']
        BaseAttr.area=houseData['houseArea']
        BaseAttr.area=houseData['houseArea']
        BaseAttr.structure=houseData['houseStyle']
        BaseAttr.inArea=houseData['avgArea']
        BaseAttr.buildType='暂无数据'
        BaseAttr.buildHead=houseData['houseHead']
        BaseAttr.buildStruct=houseData['houseStruct']
        BaseAttr.decorate=houseData['decorate']
        BaseAttr.ladderHouPro=houseData['heat']
        BaseAttr.heatMethod=houseData['houseLift']
        BaseAttr.lift='%s年'%houseData['houseYear']
        BaseAttr.period=houseData['houseBL']
        BaseAttr.address_wu=houseData['address_wu']
        BaseAttr.address_qu=houseData['address_qu']
        BaseAttr.address_detail=houseData['address_detail']
        BaseAttr.save()

        Tag.name='无'
        Tag.save()

        houseData = json.loads(houseData)
        SelecttData.houseType = houseData['houseType']

        SelecttData.area = houseData['houseArea']

        SelecttData.houseHead = houseData['houseHead']

        SelecttData.decorate = houseData['decorate']

        SelecttData.lift = '%s年' % houseData['houseYear']

        SelecttData.address_wu = houseData['address_wu']
        SelecttData.address_qu = houseData['address_qu']
        SelecttData.address_detail = houseData['address_detail']
        SelecttData.tagList='无'
        SelecttData.vides='0'
        SelecttData.save()



        Container.content=(
            houseData['houseType'],
            houseData['houseArea'],
            houseData['houseHead'],
            houseData['decorate'],
            houseData['houseYear'],
            houseData['address_wu'],
            houseData['address_qu'],
            houseData['address_qu'],
            houseData['address_detail']
        )



        return Response('ok')