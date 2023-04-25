import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Demande,Notification,CalendarEvents
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save,pre_save
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import datetime
from .models import *

def check_exceptionnelle(sender,instance,**kwargs):
    if instance.typecongee !='Exceptionnelle':
        instance.excep=None
    else:
        if instance.excep =='m':
            instance.dureeCongee=3
        elif instance.excep =='mf':
            instance.dureeCongee=1        
        elif instance.excep =='deJE':
            instance.dureeCongee=3   
        elif instance.excep =='deMP':
            instance.dureeCongee=2
        elif instance.excep =='naisE':
            instance.dureeCongee=1
        elif instance.excep =='batE':
            instance.dureeCongee=1                        
pre_save.connect(check_exceptionnelle,sender=Demande)

@receiver(post_save,sender=Demande) 
def send_mail_decision(sender,instance,**kwargs):
    destinataire = instance.user.email
    
    if instance.approuver == True and instance.decision == True:
        send_mail(
            'BNM',
            'votre demande de congé demandée le '+instance.dateCongee.strftime("%d %B %Y")+' est approuver',
            'settings.EMAIL_HOST_USER',
            [destinataire],
            fail_silently=False,
        )
    elif instance.approuver == False or instance.decision == False:
        send_mail(
            'BNM',
            'votre demande de congé demandée le '+instance.dateCongee.strftime("%d %B %Y")+' est rejeter',
            'settings.EMAIL_HOST_USER',
            [destinataire],
            fail_silently=False,
        )
   

@receiver(post_save,sender=Demande) 
def setPeriode(sender,instance,created, **kwargs):
    if instance.approuver == True and instance.decision == True :
        color = ''
        if instance.direction == 1:
            color = 'green'
        elif instance.direction == 2:
            color = 'orange'
        CalendarEvents.objects.create(
            id_d=instance,title="{} {}".format(instance.user.first_name,instance.user.last_name),
            start=instance.dateCongee,
            end=(instance.dateCongee+datetime.timedelta(instance.dureeCongee)),
            direction = instance.direction,
            backgroundColor = color
        )

@receiver(post_save,sender=User) 
def createProfile(sender,instance,created, **kwargs):
    if created :
        Profile.objects.create(user=instance)
#post_save.connect(createProfile,sender=User)
    
@receiver(post_save,sender=User) 
def updateProfile(sender,instance,created, **kwargs):
    if created == False:
        instance.profile.save()

@receiver(post_save,sender=Demande)
def notif_user(sender,instance,created,**kwargs):
    rh=Notification.objects.get(nom='rh')
    info=Notification.objects.get(nom='info')
    if instance.decision:
        rh.add_notif(instance.id)
        channel_layer=get_channel_layer()
        group_name = 'notif_menager'
        event ={
            'type':'nouvelle_demande_rh',
            'direction':'rh',
            'count':json.dumps(rh.get_notif_count()),
        }
        async_to_sync(channel_layer.group_send)(group_name,event)
        
    if created:
        info=Notification.objects.get(nom='info')
        if instance.direction.nom=='info' and instance.decision == None:
            info.add_notif(instance.id)
            channel_layer=get_channel_layer()
            group_name = 'notif_menager'
            event ={
                'type':'nouvelle_demande_info',
                'direction':'info',
                'count':json.dumps(info.get_notif_count()),
            }
            async_to_sync(channel_layer.group_send)(group_name,event)
            
            