from rest_framework import serializers

from info.models import House, Image, BaseAttr


class ImageSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('name','url')

class BaseAttrSerialzer(serializers.ModelSerializer):
    class Meta:
        model = BaseAttr
        fields = ('houseType','area','buildHead','structure','floor')
class IndexSerialzer(serializers.ModelSerializer):
    image=ImageSerialzer(many=True)
    baseAttr=BaseAttrSerialzer()
    class Meta:
        model=House
        fields = ('id','title','price','unitPrice','vide','focus','source','image','baseAttr','area','time')