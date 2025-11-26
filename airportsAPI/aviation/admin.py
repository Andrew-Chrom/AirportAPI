from django.contrib import admin
from .models import Airline, Airplane

class AirlineAdmin(admin.ModelAdmin):
    list_display = ['airline_name', 'airline_alias', 'contact_info']
    search_fields = ['airplane_name', 'airline_alias']

class AirplaneAdmin(admin.ModelAdmin):
    list_display = ['airplane_name', 'manufacturer', 'seat_num', 'commisioning_date', 'retirement_date', 'airline']
    search_fields  = ['airplane_name', 'manufacturer', 'seat_num', 'commisioning_date', 'retirement_date', 'airline']
    
admin.site.register(Airline, AirlineAdmin)
admin.site.register(Airplane, AirplaneAdmin)
