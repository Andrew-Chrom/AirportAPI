import json
from channels.generic.websocket import WebsocketConsumer
from .ai_agent import AIService

import logging

logger = logging.getLogger()

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.user = self.scope["user"]
        self.service = AIService(user=self.user)
        
        self.accept()
        
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Connected as {self.user.username}'
        }))
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        try:
            user_message = f"""<p> You: {text_data_json['message']}</p>"""
            self.send(text_data=json.dumps({
                'type': 'chat',
                'message': user_message
            }))
            
            chat_answer = self.service.get_response(text_data_json['message'])

            logger.info(f"User message: {text_data_json['message']}")
            logger.info(f'{chat_answer}')
            
            
            chat_message = f"""<p>Chat: {chat_answer}</p>"""
            
            self.send(text_data=json.dumps({
                'type': 'chat',
                'message': chat_message
            }))
        except Exception as e:
            logger.info(f'{e}')