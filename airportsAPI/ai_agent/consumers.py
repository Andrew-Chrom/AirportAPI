import json
from channels.generic.websocket import WebsocketConsumer
from .ai_agent import AIService

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()
        
        self.service = AIService()
        
        self.send(text_data=json.dumps({
                'type': 'connection_established',
                'message': 'Succesfully connected!'
        }))    
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        try:
            chat_answer = self.service.get_response(text_data_json['message'])
            
            print(f'{text_data_json['message']}')
            print(f'{chat_answer}')
            
            message = f"""<p> You: {text_data_json['message']}</p><p>Chat: {chat_answer}</p>"""
            
            self.send(text_data=json.dumps({
                'type': 'chat',
                'message': message
            }))
        except Exception as e:
            print(f'{e}')