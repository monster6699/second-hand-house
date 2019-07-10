from house.settings import dev
from django.conf import settings
from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from oauth.QQUserSerializer import QQUserSerializer
from oauth.models import OAuthQQUser
from itsdangerous import TimedJSONWebSignatureSerializer as TJS
#跳转页面
from users.models import User
#微博接口调用

import json

class OuthQQView(APIView):
    def get(self,request):
        #获取查询字符串内容
        state = request.query_params.get('next')
        if not state:
            state='/'
        #调用接口
        qq = OAuthQQ(client_id=dev.QQ_CLIENT_ID,client_secret=settings.QQ_CLIENT_SECRET,redirect_uri=dev.QQ_REDIRECT_URI,state=state)
        #获取跳转页面
        login_url = qq.get_qq_url()
        return Response({'login_url':login_url})

#获取openid验证用户是否绑定
class QQUserView(CreateAPIView):
    serializer_class =QQUserSerializer
    def get(self,request):
        #获取code值
        code = request.query_params.get('code')
        if not code:
            return Response({'error':'code获取错误'})
        #通过code值获取access_token值
        qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,client_secret=settings.QQ_CLIENT_SECRET,redirect_uri=settings.QQ_REDIRECT_URI,state='/')
        try:
            access_token = qq.get_access_token(code)
            #通过token值获取openid
            openid = qq.get_open_id(access_token)
        except:
            return Response({'error':'code数据错误'})
        #判断用户是否绑定
        try:
            qq = OAuthQQUser.objects.get(openid=openid)
        except:
            #未绑定返回opendid并且加密
            tjs = TJS(settings.QQ_CLIENT_SECRET,300)
            opend_id = tjs.dumps({'openid':openid}).decode()
            return Response({'access_token':opend_id})
        else:
            #绑定后，返回username ,user_id, token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            user = qq.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            data={
                'username':user.username,
                'user_id':user.id,
                'token':token
            }
            response = Response(data)

            return response


