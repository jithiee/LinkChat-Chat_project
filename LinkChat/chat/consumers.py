from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Message , UserChannel
from django.contrib.auth.models import User
import datetime


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
       
        try  :
              user_channel = UserChannel.objects.get(user = self.scope.get('user'))     
              user_channel.channel_name = self.channel_name
              user_channel.save()
        
        except :
                UserChannel.objects.create(
                    user = self.scope.get('user'),
                    channel_name = self.channel_name
                )
        
        
        # print(self.scope.get('user') , 'kkkkkkkkkkk')
        
        self.person_id =   self.scope.get('url_route').get('kwargs').get('id') 
        
        
        
        
        
        
    def receive(self, text_data):
        # print(text_data )
        # print(text_data.get('type'))
        # print(text_data.get('message'))
        
        text_data = json.loads(text_data)
        to_whos = User.objects.get(id = self.person_id)
        
        
        if text_data.get('type') == 'new_message':
            
                now = datetime.datetime.now()
                date = now.date()
                time = now.time()
                
                Message.objects.create(
                    from_who = self.scope.get('user'),
                    to_who = to_whos ,
                    date = date,
                    time = time ,
                    message = text_data.get('message'), 
                    has_been_seen = False
                    
                )
                
                try:
                    
                    user_channel_name  = UserChannel.objects.get(user = to_whos)
                        
                    data = {
                        "type" : "receiver_function",
                        "type_of_data" :"new_message",
                        "data" :text_data.get('message')
                    }
                    
                    async_to_sync(self.channel_layer.send)( user_channel_name.channel_name , data )
                    
                except :
                    pass
        elif text_data.get('type')   == 'i_have_seen_this_message':

                try:
                    
                    user_channel_name  = UserChannel.objects.get(user = to_whos)
                        
                    data = {
                        "type" : "receiver_function",
                        "type_of_data" :"the_message_have_been_seen_from_the_other",
                       
                    }
                    
                    async_to_sync(self.channel_layer.send)( user_channel_name.channel_name , data )
                 
                    
                except :
                    pass

                
                    
                
        
        
        
       
       
    #    self.send('{"type":"msg arreied/reached": "status:"reached" }')
       
    # def disconnect(self, code):
    #     print(code)
    #     print("the connection is losted or disconected  ")

    def receiver_function(self , the_data_come_from_the_layer):
        print('ooooooooooo')
        print(the_data_come_from_the_layer ,'jjoo')
        # print(the_data_come_from_the_layer.get('message'))
        # print(the_data_come_from_the_layer.get('my first name'))
        data = json.dumps(the_data_come_from_the_layer)
        self.send(data)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # these are from connect function 
        
        
        
         # self.send('{"type":"accept" , "status":"accepted"}')
        # print(self.scope)
        # print(self.scope.get("user").id)
        # print(self.scope.get("user").email)
        # print(self.scope.get("user").first_name)
        # print(self.scope.get("user").last_name)
     
        # print(self.scope.get("session").get("get_me_from_the_consumer"))
        # print(self.scope.get("url_route"))
        # print(self.scope.get("url_route").get("kwargs").get("name"))
        # print(self.channel_layer)
        # print(type(self.channel_layer))
        # print(self.channel_name)
        # print(self.channel_layer.channels)
        # async_to_sync(self.channel_layer.group_add)("momo_group" , self.channel_name) 
        # print(self.channel_layer.groups)       
        # data = {
        #     "type":"receiver_function",
        #     "message":"hi man this is me",
        #     "my first name" :"jithin"
        # }
        
        # async_to_sync(self.channel_layer.send)(self.channel_name , data)
        # async_to_sync(self.channel_layer.group_add)("test" , self.channel_name )
        