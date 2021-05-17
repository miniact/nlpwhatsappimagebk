# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import Chatroom
# import json

# class ChatRoomConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_id = self.scope['url_route']['kwargs']['room_id']
#         print("ASYNC Rid: ",self.room_id,type(self.room_id))
#         try:
#             roomobj = Chatroom.get(pk=self.room_id)
#             self.room_group_name = ''.join(roomobj.room_name.split()) + self.room_id
#             #uniquely identifys the room 


#             await self.channel_layer.group_add(
#                 self.room_group_name, self.room_id           
#             )
#             await self.accept()

#             await self.channel_layer.group_send(self.room_group_name, {
#                 'type': 'first_message',
#                 'data': 'Hello form WS!',
#             })

#         except :
#             print("err")


#     async def first_message(self, event):
#         data = event['data']

#         await self.send(text_data=json.dumps({
#             'first': data 
#         }))

#     #leave channel
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard( self.room_group_name, self.room_id )
#     # def connect(self):
#     #     self.accept()

#     # def disconnect(self, close_code):
#     #     pass

#     # def receive(self, text_data):
#     #     text_data_json = json.loads(text_data)
#     #     message = text_data_json['message']

#     #     self.send(text_data=json.dumps({
#     #         'message': message
#     #     }))