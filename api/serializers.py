from .models import Language, Location, Information
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = [
            'code',
            'name',
            'native'
        ]


class LocationSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True)

    class Meta:
        model = Location
        fields = [
            'geoname_id',
            'capital',
            'country_flag',
            'country_flag_emoji',
            'country_flag_emoji_unicod',
            'calling_code',
            'is_eu',
            'languages',
        ]


class InformationSerializer(serializers.ModelSerializer):
    location = LanguageSerializer()

    class Meta:
        model = Information
        fields = [
            'id',
            'ip',
            'type',
            'continent_code',
            'continent_name',
            'country_code',
            'country_name',
            'region_code',
            'region_name',
            'city',
            'zip',
            'latitude',
            'longitude',
            'location'
        ]
