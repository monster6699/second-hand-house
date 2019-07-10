import re
from django_redis import get_redis_connection
from  rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from info.models import Image, BaseAttr, House
from users.models import User


class UserSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=12,min_length=6,write_only=True)
    sms_code = serializers.CharField(max_length=6,min_length=6,write_only=True)
    allow = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields=('id','username','mobile','password','password2','allow','sms_code')
        extra_kwargs={
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    #验证手机号
    def validated_mobile(self,value):
        if not re.match(r'1[3-9]\d{9}',value):
            raise serializers.ValidationError("手机号格式错误")
        return value
    #验证两次密码是否一致
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("两次密码不一致")

        #连接redis

        conn = get_redis_connection("sms_code")
        redis_mobile = conn.get("sms_code%s"%attrs['mobile'])
        if redis_mobile is None:
            return serializers.ValidationError("验证码已过期")
        if attrs['sms_code'] !=redis_mobile.decode():
            return serializers.ValidationError("验证码错误")
        return attrs
    #验证用户是否同意协议
    def validated_allow(self,value):
        if value!=True:
            raise serializers.ValidationError("未同意协议")

    def create(self, validated_data):
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user


class ImageSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('name','url')

class BaseAttrSerialzer(serializers.ModelSerializer):
    class Meta:
        model = BaseAttr
        fields = ('houseType','area','buildHead','structure','floor')
class GetHistorySerialzer(serializers.ModelSerializer):
    image=ImageSerialzer(many=True)
    baseAttr=BaseAttrSerialzer()
    class Meta:
        model=House
        fields = ('id','title','price','unitPrice','vide','focus','source','image','baseAttr','area','time')
