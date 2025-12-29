from google import genai
from google.genai import types
from django.conf import settings
from flights.models import Flight, Order
from django.db.models.aggregates import Min
import datetime
import json
from django.utils import timezone

def search_flights(destination: str, departure_city: str = None, date_from: str = None, date_to: str = None):
    flights = Flight.objects.filter(
        arrival_airport__city__icontains=destination,
        flight_status='scheduled'
    )

    if departure_city:
        flights = flights.filter(departure_airport__city__icontains=departure_city)

    if date_from and date_to:
        flights = flights.filter(departure_time__date__range=[date_from, date_to])
    elif date_from:
        flights = flights.filter(departure_time__date=date_from)
    else:
        today = timezone.now().date()
        flights = flights.filter(departure_time__date__gte=today)

    flights = flights.order_by('departure_time')[:5]

    data = []
    for f in flights:
        data.append({
            "id": f.id,
            "route": f"{f.departure_airport.city} -> {f.arrival_airport.city}",
            "departure_time": f.departure_time.strftime('%Y-%m-%d %H:%M'),
            "arrival_time": f.arrival_time.strftime('%Y-%m-%d %H:%M'),
            "status": f.flight_status,
        })

    if not data:
        return "No flights found."

    return json.dumps(data)


def get_user_orders(email: str):
    orders = Order.objects.filter(user__email__iexact=email).order_by('-created_at')[:5]
    
    if not orders.exists():
        return "No orders found."
    
    data = []
    for o in orders:
        tickets_info = []
        for t in o.tickets.all():
            tickets_info.append({
                "flight": f"{t.flight.departure_airport.city} -> {t.flight.arrival_airport.city}",
                "date": t.flight.departure_time.strftime('%Y-%m-%d'),
                "seat": f"{t.row}{t.column}",
                "type": t.ticket_type
            })

        data.append({
            "order_id": o.id,
            "status": o.status,
            "total_price": o.amount,
            "tickets": tickets_info
        })
        
    return json.dumps(data)



def get_ticket_details(flight_id: int):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        return "Flight ID not found."

    available = flight.ticket_set.filter(ticket_status='available')
    total_free = available.count()

    if total_free == 0:
        return "No seats available."

    prices = {}  
    for t_type in ['economy', 'business']:
        min_price = available.filter(ticket_type=t_type).aggregate(Min('price'))['price__min']
        if min_price:
            prices[t_type] = min_price

    response_data = {
        "flight_id": flight.id,
        "available_seats": total_free,
        "prices": prices
    }
    
    return json.dumps(response_data)

class AIService:
    def __init__(self, user):

        self.user = user

        with open('./ai_agent/prompt.txt', 'r', encoding='utf-8') as f:
            prompt = f.read()

        today = datetime.date.today().strftime("%Y-%m-%d")
        weekday = datetime.date.today().strftime("%A")

        time_context = f"""\nSYSTEM CONTEXT:\n Today is {weekday}, {today}.\n 
                        When user says 'next week' or 'tomorrow', 
                        calculate dates based on today.\n"""
        
        
        user_context = f"""\n--- CURRENT USER CONTEXT ---\n"
                Username: {user.username}\n
                Email: {user.email}\n
                ------------------------------\n"""
        
        prompt += time_context + user_context

        self.client = genai.Client()
        self.config = types.GenerateContentConfig(
            tools=[search_flights, get_ticket_details, get_user_orders],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False, 
                maximum_remote_calls=3
            ),
            
            system_instruction=prompt
        )
        
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",#"gemini-1.5-flash-latest",
            config=self.config
        )

    def get_response(self, user_message):
        try:
            
            response = self.chat.send_message(user_message)
            return response.text
        except Exception as e:
            return f"Error: {e}"