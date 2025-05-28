from django.db import models  

class Scheme(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_year = models.IntegerField()

class State(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2)
    # Remove geo_data field or replace with:
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

class SchemeData(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    beneficiaries = models.IntegerField()
    year = models.IntegerField()