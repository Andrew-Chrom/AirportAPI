from django.contrib import admin
from .models import Airline, Airplane, Country, Airport

class AirlineAdmin(admin.ModelAdmin):
    list_display = ['name', 'alias', 'contact_info']
    search_fields = ['name', 'alias']

class AirplaneAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer', 'max_row', 'max_column', 'commisioning_year', 'airline']
    search_fields  = ['name', 'manufacturer', 'max_row', 'max_column', 'commisioning_year', 'airline']
    
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'region']
    list_filter = ['region']
    
class AirportAdmin(admin.ModelAdmin):
    list_display = ['name', 'longitude', 'latitude', 'runaway_num', 'plane_num', 'country', 'list_airlines'] # 'airlines'
    search_fields = ['name', 'country__name', 'airlines__alias']
    list_filter = ['country__region']
    
    def list_airlines(self, obj):
        return ", ".join([airline.airline_alias for airline in obj.airlines.all()])

    list_airlines.short_description = 'Airlines'

admin.site.register(Airline, AirlineAdmin)
admin.site.register(Airplane, AirplaneAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Airport, AirportAdmin)