from rest_framework import serializers

from info.models import House


class DetailSerilazer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ("id")