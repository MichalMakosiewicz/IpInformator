from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    native = models.CharField(max_length=20)


class Location(models.Model):
    geoname_id = models.IntegerField(primary_key=True)
    capital = models.CharField(max_length=20)
    languages = models.ManyToManyField(Language, related_name='languages')
    country_flag = models.URLField()
    country_flag_emoji = models.CharField(max_length=20)
    country_flag_emoji_unicode = models.CharField(max_length=20)
    calling_code = models.CharField(max_length=20)
    is_eu = models.BooleanField()


class Information(models.Model):
    ip = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    continent_code = models.CharField(max_length=20)
    continent_name = models.CharField(max_length=20)
    country_code = models.CharField(max_length=10)
    country_name = models.CharField(max_length=20)
    region_code = models.CharField(max_length=20)
    region_name = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    zip = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.ForeignKey(Location, related_name='location', on_delete=models.CASCADE)
