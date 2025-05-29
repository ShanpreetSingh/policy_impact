from django.db import models

class Scheme(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2)
    
class SchemeData(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    beneficiaries = models.IntegerField()
    year = models.IntegerField()