from django.core import serializers
from rest_framework.response import Response
from rest_framework import generics
from .models import Information, Language, Location
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
import json
import requests
from secret import ipstac_ulr, ipstack_api_key
from rest_framework import status
from django.forms.models import model_to_dict


def get_query_or_object(model_instance, item_id):
    if item_id != 0 and item_id != '':
        try:
            object_ins = model_instance.objects.get(pk=item_id)
            return Response(model_to_dict(object_ins), status=status.HTTP_200_OK)
        except model_instance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    queryset = model_instance.objects.all()
    data = json.loads(serializers.serialize('json', queryset))
    return Response(data, status=status.HTTP_200_OK)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class InformationViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, inf_id=0):
        return get_query_or_object(Information, inf_id)

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        ip = body['ip']
        url = ipstac_ulr + ip + '?access_key=' + ipstack_api_key
        try:
            response = requests.get(url)
            if response.status_code == 200:
                ip_data = json.loads(response.content)
                location = ip_data.pop('location')
                languages = location.pop('languages')
                try:
                    location = Location.objects.get(pk=location.get('geoname_id'))
                except Location.DoesNotExist:
                    location = Location.objects.create(**location)
                for language in languages:
                    try:
                        lang = Language.objects.get(pk=language.get('code'))
                    except Language.DoesNotExist:
                        lang = Language.objects.create(**language)
                    location.languages.add(lang)
                information = Information.objects.create(**ip_data, location=location)
                print(model_to_dict(information))
                return Response(model_to_dict(information), status=status.HTTP_201_CREATED)
            else:
                raise Exception("Request failure")
        except Exception as e:
            print(e)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LanguageViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, lang_id=''):
        return get_query_or_object(Language, lang_id)


class LocationViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, loc_id=0):
        return get_query_or_object(Location, loc_id)
