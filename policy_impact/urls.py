from django.urls import path
from django.views.generic import TemplateView
from schemes import views as scheme_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),  # Frontend
    path('api/schemes/', scheme_views.scheme_list),  # API endpoint
]