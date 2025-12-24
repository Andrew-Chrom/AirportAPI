# import google.generativeai as genai
from google import genai
from google.genai import types
from django.conf import settings
from flights.models import Flight
from django.db.models.aggregates import Min

with open('./ai_agent/prompt.txt', 'r', encoding='utf-8') as f:
    prompt = f.read()


def search_flight_with_tickets(destination: str, date:str = None):
    flights = Flight.objects.filter(
        arrival_airport__city__icontains=destination, 
        flight_status='scheduled'
    )
    
    if date:
        flights = flights.filter(departure_time__date=date)
        
    if not flights.exists():
        return f"На жаль, рейсів до {destination} не знайдено."

    response_text = []

    for f in flights:
        available_tickets = f.tickets.filter(ticket_status='available')
        count = available_tickets.count()
        
        if count == 0:
            response_text.append(f"Рейс до {destination} ({f.departure_time}) - МІСЦЬ НЕМАЄ.")
            continue
        
        min_price = available_tickets.aggregate(Min('price'))['price__min']
        
        info = (
            f"Рейс: {f.departure_airport.city} -> {f.arrival_airport.city}\n"
            f"Час: {f.departure_time.strftime('%H:%M')}\n"
            f"Статус: {f.get_flight_status_display()}\n"
            f"Вільних місць: {count}\n"
            f"Ціна від: ${min_price}"
        )
        response_text.append(info)

    return "\n---\n".join(response_text)


class AIService:
    def __init__(self):
        self.available_tools = {
            'search_flights': search_flight_with_tickets
        }
        self.client = genai.Client()
        self.config = types.GenerateContentConfig(
            tools=[search_flight_with_tickets],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False, 
                maximum_remote_calls=3
            ),
            
            system_instruction=prompt
        )
        
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash-lite",#"gemini-1.5-flash-latest",
            config=self.config
        )

    def get_response(self, user_message):
        try:
            
            response = self.chat.send_message(user_message)
            # response = self.chat.send_message(user_message)
            return response.text
        except Exception as e:
            return f"Error: {e}"