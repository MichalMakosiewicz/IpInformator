from rest_framework.response import Response
from rest_framework import generics
from .models import Information, Language, Location
from .serializers import UserSerializer, InformationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
import json
import requests
from secret import ipstac_ulr, ipstack_api_key
from rest_framework import status
from django.forms.models import model_to_dict


def get_nested(model_instance):
    data = model_to_dict(model_instance)
    languages = []
    location = model_to_dict(Location.objects.get(pk=data['location']))
    for language in location['languages']:
        lang = model_to_dict(language)
        languages.append(lang)
    location['languages'] = languages
    data['location'] = location
    return data


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class InformationViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, inf_id=0):
        if inf_id != 0 and inf_id != '':
            try:
                object_ins = Information.objects.get(pk=inf_id)
                return Response(get_nested(object_ins), status=status.HTTP_200_OK)
            except Information.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        queryset = Information.objects.all()
        nested_data = []
        for data in queryset:
            nested_data.append(get_nested(data))
        return Response(nested_data, status=status.HTTP_200_OK)

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
                    location = Location.objects.get(id=location.get('geoname_id'))
                except Location.DoesNotExist:
                    location = Location.objects.create(**location)
                for language in languages:
                    try:
                        lang = Language.objects.get(pk=language.get('code'))
                    except Language.DoesNotExist:
                        lang = Language.objects.create(**language)
                    location.languages.add(lang)
                information = Information.objects.create(**ip_data, location=location)
                return Response(get_nested(information), status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, inf_id):
        ip_data = json.loads(request.body)
        location = ip_data.pop('location')
        try:
            location_instance = Location.objects.get(pk=location['geoname_id'])
            location.pop('geoname_id')
            languages = location.pop('languages')
            for key, value in location.items():
                location_instance.update_field(key, value)
                location_instance.save(update_fields=location.keys())
            information = Information.objects.get(pk=inf_id)
            for key, value in ip_data.items():
                information.update_field(key, value)
                information.save(update_fields=ip_data.keys())
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)