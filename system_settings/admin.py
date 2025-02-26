from django.contrib import admin
from .models import *

class SettingAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False
    def has_add_permission(self, request, obj=None):
        #Disable add
        return False

admin.site.register(Setting, SettingAdmin)
