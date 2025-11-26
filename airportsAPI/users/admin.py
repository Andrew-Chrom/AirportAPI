from django.contrib import admin
from .models import CustomUser

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_staff', 'is_active', 'phone_number']
    search_fields = ['username', 'first_name', 'last_name']
    
admin.site.register(CustomUser, UserAdmin)