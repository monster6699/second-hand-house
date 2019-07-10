import re
from django.conf import settings
from django_redis import get_redis_connection
from rest_framework import serializers
from itsdangerous import TimedJSONWebSignatureSerializer as TJS
from rest_framework_jwt.settings import api_settings

from users.models import User
from oauth.models import OAuthQQUser


class QQUserSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(max_length=6,min_length=6,write_only=True)
    token = serializers.CharField(read_only=True)
    mobile =serializers.CharField(max_length=11)
    access_token=serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id','username', 'password', 'sms_code','mobile','token','access_token')
        extra_kwargs = {
           'password': {
               'max_length': 20,
               'min_length': 8,
               'write_only': True
           },
           'username': {
               'read_only':True
           },
        }

    #验证手机号
    def validate_mobile(self, value):
        if not re.match(r'1[3-9]\d{9}$',value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate(self, attrs):

        #验证短信验证码'
        conn = get_redis_connection('sms_code')
        mobile_code = conn.get('sms_code%s'%attrs['mobile'])
        if mobile_code is None:
            raise serializers.ValidationError('验证码已过期')
        if mobile_code.decode() != attrs['sms_code']:
            raise  serializers.ValidationError("验证码错误")
        #解密openid
        print(type(attrs['access_token']))
        tjs = TJS(settings.QQ_CLIENT_SECRET,300)
        try:
            data = tjs.loads(attrs['access_token'])
            print(data)
        except Exception as e:
            print(e)
            raise serializers.ValidationError("openid解码错误")
        openid = data['openid']
        if not openid:
            raise serializers.ValidationError("openid获取失败")
        attrs['openid'] = openid
        #通过openid验证用户是否绑定
        try:
            user = User.objects.get(mobile=attrs['mobile'])
        except:
            #用户未绑定
            return attrs
        else:
            attrs['user']= user
            return attrs
            #用户绑定
    def create(self, validated_data):
        user = validated_data.get('user')
        if not user:
            #用户未绑定，进行保存
            user = User.objects.create_user(username=validated_data['mobile'],password=validated_data['password'],mobile=validated_data['mobile'])

        #用户绑定
        OAuthQQUser.objects.create(user=user,openid = validated_data['openid'])


        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user
