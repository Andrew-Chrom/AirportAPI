from django.contrib import admin
from .models import Country, Airport

class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_name', 'region']
    list_filter = ['region']
    
class AirportAdmin(admin.ModelAdmin):
    list_display = ['name', 'longitude', 'latitude', 'runaway_num', 'plane_num', 'country', 'list_airlines'] # 'airlines'
    search_fields = ['name', 'country__country_name', 'airlines__airline_alias']
    list_filter = ['country__region']
    
    def list_airlines(self, obj):
        return ", ".join([airline.airline_alias for airline in obj.airlines.all()])

    list_airlines.short_description = 'Airlines'

admin.site.register(Country, CountryAdmin)
admin.site.register(Airport, AirportAdmin)