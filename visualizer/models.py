# visualizer/models.py
from django.db import models
from django.contrib.auth.models import User

class State(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Scheme(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    start_year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class PolicyData(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    year = models.IntegerField()
    beneficiaries = models.PositiveIntegerField()
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('state', 'scheme', 'year')
        verbose_name_plural = "Policy Data"
    
    def __str__(self):
        return f"{self.scheme} in {self.state} ({self.year})"