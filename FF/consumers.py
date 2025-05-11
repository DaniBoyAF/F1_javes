import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TelemetryConsumer(AsyncWebsocketConsumer):
      async def connect(self):#esse async é para permitir que o código seja executado e vc pode dar delay
            # Accept the WebSocket connection
            await self.accept()
            await self.send(text_data=json.dumps({
                  'message': 'Conectado ao WebSocket de Telemetria!'
            }))

      async def disconnect(self, close_code):
            pass
      
      async def receive(self,text_data):
            data= json.loads(text_data)
            #processar dados recebidos
            await self.send(text_data=json.dumps({
                  'message': 'Dados recebidos com sucesso!',
                  'data': data
            }))