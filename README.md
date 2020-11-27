# IP info collector

Web Ip geological data collector.

##Summary

The aim of this task is to build an API (backed by any kind of database) that requires JWT authorization. The application should be able to store geolocation data in the database, based on IP address or URL - you can use https://ipstack.com/ to get geolocation data (you can obtain free API KEY here -> https://ipstack.com/signup/free). The API should be able to add, delete or provide geolocation data on the base of ip address or URL.

##Setup

Requirements:
    
`Docker`

In root dir:

run `docker-compose up`

##Endpoints

###Authorization

Method: JSON Web Token (https://en.wikipedia.org/wiki/JSON_Web_Token)

Register new users:

`/api/account/register/`
 
    Formd-data:
    {
        username: <username>,
        password: <password>
    }

Response:

    {
        "username": <username>"
    }

User authorization:
 
`/api/token/`

Formd-data:

    {
        username: <username>,
        password: <password>
    }

Response:

    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwNjUyNzAyMywianRpIjoiODRiM2ZlMmZhNzU0NDU0ZTg4NGU1ZWIxZDQ4NTkwYTEiLCJ1c2VyX2lkIjoxfQ.TL6keHCN6KvkckhFMjqsGVaf2OU5xdTw6KMXezQeWk8",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2NDQwOTIzLCJqdGkiOiIzZTI2MGFkMTM2MDc0YTVhODQ1ZWZiZjc2NGZhM2FlMCIsInVzZXJfaWQiOjF9.dzqE-kC1TfPRUfObUNAnHa1yWjMudT9SO8hCmeaBkVQ"
    }
    
### Usage

Gahter new data:

`POST` `/api/info/`

    Body:
    {
        "ip": "<IP>"
    }
    
Response:

    {
        "id": 3,
        "ip": "89.68.131.22",
        "type": "ipv4",
        "continent_code": "EU",
        "continent_name": "Europe",
        "country_code": "PL",
        "country_name": "Poland",
        "region_code": "PM",
        "region_name": "Pomerania",
        "city": "Gdynia",
        "zip": "81-004",
        "latitude": 54.540679931640625,
        "longitude": 18.46780014038086,
        "location": 3099424 - Object ID
    }
    
`GET` `/api/info/?<int:id>`

    Body:
    {
        "ip": "<IP>"
    }
    
Response:

    [
        {
            "id": 3,
            "ip": "89.68.131.22",
            "type": "ipv4",
            "continent_code": "EU",
            "continent_name": "Europe",
            "country_code": "PL",
            "country_name": "Poland",
            "region_code": "PM",
            "region_name": "Pomerania",
            "city": "Gdynia",
            "zip": "81-004",
            "latitude": 54.540679931640625,
            "longitude": 18.46780014038086,
            "location": 3099424 - Object ID
        }
    ]
    
`GET` `/api/location/?<id:int>`

Response:

    [
        {
            "model": "api.location",
            "pk": 3099424,
            "fields": {
                "capital": "Warsaw",
                "country_flag": "http://assets.ipstack.com/flags/pl.svg",
                "country_flag_emoji": "🇵🇱",
                "country_flag_emoji_unicode": "U+1F1F5 U+1F1F1",
                "calling_code": "48",
                "is_eu": true,
                "languages": [
                    "pl" - Object ID
                ]
            }
        }
    ]
    
`GET` `/api/language/?<id>`

Response:

    [
        {
            "model": "api.language",
            "pk": "pl",
            "fields": {
                "name": "Polish",
                "native": "Polski"
            }
        }
    ]