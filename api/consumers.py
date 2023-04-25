import json
import jwt
from urllib.parse import parse_qs

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *

class NotificationConsumer(WebsocketConsumer):  
    def connect(self):
        # self.user = jwt.decode(self.scope['query_string'],"secret",algorithm="HS256")
        self.user = self.scope['query_string'].decode('utf-8').split('=')[1]
        self.user = jwt.decode(self.user,options={'verify_signature':False})
        self.group_name = 'notif_menager'
       
        async_to_sync(self.channel_layer.group_add)(
           self.group_name,self.channel_name    
        )
       
        rh = Notification.objects.get(nom='rh')
        info = Notification.objects.get(nom='info')  
        if rh.responsable.filter(username=self.user['username']).count()>0:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type':'nouvelle_demande_rh',
                    'direction':'rh',
                    'count':json.dumps(rh.get_notif_count()),
                }
            )
        elif info.responsable.filter(username=self.user['username']).count()>0:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type':'nouvelle_demande_info',
                    'direction':'info',
                    'count':json.dumps(info.get_notif_count()),
                }
            ) 
        self.accept()
        
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,self.channel_name
        ) 
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json["type"]
        
        if type == 'delete':
            rh = Notification.objects.get(nom='rh')
            info = Notification.objects.get(nom='info')  
            if rh.responsable.filter(username=self.user['username']).count()>0:
                rh.nettoyage()
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        'type':'nouvelle_demande_rh',
                        'direction':'rh',
                        'count':json.dumps(rh.get_notif_count()),
                    }
                )
            elif info.responsable.filter(username=self.user['username']).count()>0:
                info.nettoyage()
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        'type':'nouvelle_demande_info',
                        'direction':'info',
                        'count':json.dumps(info.get_notif_count()),
                    }
                ) 

            # self.send(text_data=json.dumps({"message": message})) 
        
    def nouvelle_demande_rh(self,event):
        rh = Notification.objects.get(nom='rh')
        if rh.responsable.filter(username=self.user['username']).count()>0:
            self.send(text_data=json.dumps(event)) 
          
    def nouvelle_demande_info(self,event):
        info = Notification.objects.get(nom='info')
        if info.responsable.filter(username=self.user['username']).count()>0:
            self.send(text_data=json.dumps(event)) 
          