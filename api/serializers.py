from rest_framework import serializers
from django.utils.text import gettext_lazy as _
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only = True)
    class Meta:
        model = User
        fields = ["id",'first_name','last_name','email','is_superuser','username','profile']

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'
        
class PostSerializer(serializers.ModelSerializer):
    direction = DirectionSerializer()
    class Meta:
        model = Direction
        fields = ['id','direction','nom']
      
class DemandeSerializer(serializers.ModelSerializer):
     class Meta:
        model = Demande
        fields = '__all__'
        
class InfoRHSerializer(serializers.ModelSerializer):
    #demande = DemandeSerializer
    class Meta:
        model = InfoRH
        fields = ['id', 'demande','solde_jours','jours_date','visa_rh','visa_drh','date','comentaire']
        

class SetDemandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demande
        fields = ['user','dateCongee','dureeCongee','typecongee','commentair','nbenf','excep','direction','decision']
class UpdateDemandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demande
        fields = ['approuver','decision','decisioner_by']


class InfoDemandeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    direction = DirectionSerializer()
    class Meta:
        model = Demande
        fields = ['id','nbenf','excep','user','dateCongee','dureeCongee','typecongee','commentair','decision','decisioner_by','created_date','created_time','nbenf','direction','approuver']

class CalendarSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    direction = DirectionSerializer()
    class Meta:
        model = Demande
        fields = ['id','user','dateCongee','dureeCongee','nbenf','direction']
        
        
class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
            
class CalendarEventsSerializer(serializers.ModelSerializer):
    id_d = DemandeSerializer()
    class Meta:
        model = CalendarEvents
        fields = ['id','title','start','end','direction','backgroundColor','id_d']
    
 