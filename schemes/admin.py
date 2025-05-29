from django.contrib import admin
from .models import Scheme, State, SchemeData

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)

@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(SchemeData)
class SchemeDataAdmin(admin.ModelAdmin):
    list_display = ('scheme', 'state', 'year', 'beneficiaries')
    list_filter = ('scheme', 'state', 'year')
    search_fields = ('state__name', 'scheme__name')