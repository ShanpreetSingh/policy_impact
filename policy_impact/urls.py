from django.urls import path
from django.contrib import admin
from django.urls import path, include
from schemes import views
from django.views.generic import TemplateView
from schemes import views as scheme_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schemes/', scheme_views.scheme_list),
    path('api/states/', scheme_views.state_list),
    path('api/state/<str:state_code>/', scheme_views.state_impact),
    path('', TemplateView.as_view(template_name='index.html')),
]