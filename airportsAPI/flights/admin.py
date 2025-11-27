from django.contrib import admin
from .models import Flight, Ticket

class FlightAdmin(admin.ModelAdmin):
    list_display = ['plane', 'departure_airport', 'arrival_airport','departure_time', 'arrival_time', 'flight_status']
    list_filter = ['flight_status']
    list_editable = ['flight_status']
    
class TicketAdmin(admin.ModelAdmin):
    list_display = ['flight__departure_airport__name', 'flight__arrival_airport__name', 'price', 'row', 'column', 'ticket_type', 'ticket_status']
    list_filter = ['ticket_type', 'ticket_status']
    search_fields = ['flight__departure_airport__name', 'flight__arrival_airport__name']
    list_editable = ['ticket_status', 'ticket_type']
    
admin.site.register(Flight, FlightAdmin)
admin.site.register(Ticket, TicketAdmin)