import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .ai_agent import AIService

import logging

logger = logging.getLogger()

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return
        
        self.service = AIService(user=self.user)
        
        await self.accept()
        
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Connected as {self.user.username}'
        }))
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        try:
            user_message = f"""<p> You: {text_data_json['message']}</p>"""
            await self.send(text_data=json.dumps({
                'type': 'chat',
                'message': user_message
            }))
            
            # chat_answer = self.service.get_response(text_data_json['message'])
            chat_answer = await database_sync_to_async(self.service.get_response)(user_message)
            
            logger.info(f"User message: {text_data_json['message']}")
            logger.info(f'{chat_answer}')
            
            
            chat_message = f"""<p>Chat: {chat_answer}</p>"""
            
            await self.send(text_data=json.dumps({
                'type': 'chat',
                'message': chat_message
            }))
        except Exception as e:
            logger.info(f'{e}')