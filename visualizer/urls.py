# visualizer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/schemes/', views.get_schemes, name='get_schemes'),
    path('api/states/', views.get_states, name='get_states'),
    path('api/submit/', views.submit_data, name='submit_data'),
]