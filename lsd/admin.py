from django.contrib import admin
from .models import LsdSurvey, LsdOrganization

# Register your models here.
class LsdOrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'parent', 'created_at', 'updated_at']
    search_fields = ['name', 'code']
    list_filter = ['created_at', 'updated_at']
    ordering = ['code']

admin.site.register(LsdOrganization, LsdOrganizationAdmin)
admin.site.register(LsdSurvey)
