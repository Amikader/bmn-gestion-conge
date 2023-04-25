from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import datetime
from .constants import types,exceptionnelle,directions,posts

class Direction(models.Model):
     nom = models.CharField(max_length=200,choices=directions,null=True)
     responsable = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
     
     def __str__(self):
         return f'{self.nom}'
     
class Post(models.Model):
    direction = models.ForeignKey(Direction,on_delete=models.CASCADE,null=True,blank=True)
    nom = models.CharField(max_length=200,choices=posts,null=True)

    def __str__(self):
        return f'{self.nom} {self.direction}'
   
def upload_photo(instance,filename):
         return 'images/{filename}'.format(filename=filename)
         
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True, null=True)
    dateCommance = models.DateField(blank=True, null=True)
    matricule = models.PositiveIntegerField(null=True)
    photo = models.ImageField(upload_to=upload_photo, null=True)
    gender = models.CharField(max_length=200,choices=(('F','Femme'),('H','Homme')),null=True)
    Poste = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    direction = models.ForeignKey(Direction,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self) :
        return f'{self.user.username}'
         
    
class Demande(models.Model):
    user = models.ForeignKey(User,related_name='owner',on_delete=models.CASCADE)
    direction = models.ForeignKey(Direction,related_name='direction',on_delete=models.CASCADE,null=True)
    typecongee = models.CharField(max_length=100,choices=types)
    excep =models.CharField(max_length=100,choices=exceptionnelle,null=True)
    commentair = models.CharField(max_length=300,null=True,blank=True)
    nbenf = models.PositiveIntegerField(default=0)
    dateCongee = models.DateField()
    dureeCongee = models.IntegerField()
    decision = models.BooleanField(null=True,blank=True)
    approuver=models.BooleanField(null=True,blank=True)
    decisioner_by = models.ForeignKey(User,related_name='decisioner',on_delete=models.CASCADE,null=True,blank=True)
    created_date = models.DateField(default=timezone.now,blank=True)
    created_time = models.TimeField(default=timezone.now,blank=True)
    
    def __str__(self):
        return f'{self.id} {self.user} {self.dateCongee} {self.dureeCongee}'
    
class Notification(models.Model):
    nom = models.CharField(max_length=128,choices=directions,unique=True)
    notif = models.ManyToManyField(to=Demande, blank=True)
    responsable = models.ManyToManyField(User, blank=True)

    def get_notif_count(self):
        return self.notif.count()
    
    def  add_notif(self,demande):
        self.notif.add(demande)
        self.save()
        
    def nettoyage(self):
        self.notif.clear()
    
    def remove_notif(self,demande):
        self.notif.remove(demande)
        

    def __str__(self):
        return f'{self.nom} ({self.get_notif_count()})'
    
class InfoRH(models.Model):
    demande = models.OneToOneField(Demande,related_name='rh',on_delete=models.CASCADE,null=True,blank=True)
    solde_jours = models.PositiveIntegerField()
    jours_date = models.PositiveIntegerField()
    visa_rh = models.CharField(max_length=30)
    visa_drh = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    comentaire = models.CharField(max_length=200,blank=True,null=True)
    
    def __str__(self):
        return f'{self.demande.id}'
        

class CalendarEvents(models.Model):
    id_d = models.OneToOneField(Demande, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start = models.DateField()
    end = models.DateField()
    direction = models.ForeignKey(Direction,on_delete=models.CASCADE,null=True)
    backgroundColor = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return f'{self.title}'
    