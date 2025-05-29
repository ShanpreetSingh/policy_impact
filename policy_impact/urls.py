from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from schemes import views as scheme_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),  # Frontend
    path('admin/', admin.site.urls),
    path('api/schemes/', scheme_views.scheme_list),  # API endpoint
]