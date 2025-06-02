# visualizer/admin.py
from django.contrib import admin
from .models import State, Scheme, PolicyData

class PolicyDataAdmin(admin.ModelAdmin):
    list_display = ('scheme', 'state', 'year', 'beneficiaries', 'submitted_by')
    list_filter = ('scheme', 'state', 'year')
    search_fields = ('scheme__name', 'state__name')
    readonly_fields = ('submission_date',)

admin.site.register(State)
admin.site.register(Scheme)
admin.site.register(PolicyData, PolicyDataAdmin)