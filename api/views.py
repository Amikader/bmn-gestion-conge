from rest_framework import viewsets,status,permissions
from .models import *
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import APIView
from .paginations import *
from rest_framework.parsers import MultiPartParser,FormParser
import json
from rest_framework.decorators import api_view
from datetime import datetime

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['group'] = user.groups.all()[0].name
        token['fname'] = user.first_name
        token['lname'] = user.last_name
        token['super'] = user.is_superuser
        d = Profile.objects.get(user=token['user_id'])
        token['direction_id'] =d.direction.id
        token['direction_nom'] =d.direction.nom
        token['post_id'] = d.Poste.id
        token['post_nom'] = d.Poste.nom
        token['gender'] = d.gender
        # ...

        return token
class  MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
 
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    


    
class DemandeViewSet(viewsets.ModelViewSet):
    queryset = Demande.objects.all()
    serializer_class = DemandeSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['dateCongee','dureeCongee','typecongee']
    filterset_fields = ['dateCongee','dureeCongee','typecongee']
    pagination_class = CustomPagination
    parser_classes=(MultiPartParser,FormParser)
    permission_classes = [permissions.DjangoModelPermissions]
    

    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['user']
    filterset_fields = ['user']
    parser_classes=(MultiPartParser,FormParser)
    permission_classes = [permissions.DjangoModelPermissions]
    
    
class InfoRHViewSet(viewsets.ModelViewSet):
    queryset = InfoRH.objects.all()
    serializer_class = InfoRHSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['demande']
    filterset_fields = ['demande']
    permission_classes = [permissions.DjangoModelPermissions]
    
    
class InfoDemandeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InfoDemandeSerializer
    queryset= Demande.objects.all()
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    search_fields = ['user__username']
    filterset_fields = ['dateCongee','dureeCongee','typecongee','decision','user','direction','approuver','user__first_name','user__profile__matricule']
    pagination_class = CustomPagination
    ordering_fields = ['id']
    ordering = ['id']
    permission_classes = [permissions.DjangoModelPermissions]
    

class UpdateDemandeViewSet(viewsets.ModelViewSet):
    serializer_class = UpdateDemandeSerializer
    queryset = Demande.objects.all()
    permission_classes = [permissions.DjangoModelPermissions]
    

class SetDemandeViewSet(viewsets.ModelViewSet):
    serializer_class = SetDemandeSerializer
    queryset = Demande.objects.all()
    permission_classes = [permissions.DjangoModelPermissions]
    
     
class NewDemandeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InfoDemandeSerializer
    queryset = Demande.objects.filter(decision=None)
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    search_fields = ['dateCongee','dureeCongee','typecongee','user','direction']
    filterset_fields = ['dateCongee','dureeCongee','typecongee','user','direction','user__first_name','user__profile__matricule']
    pagination_class = CustomPagination
    ordering_fields = ['id']
    ordering = ['id']
    permission_classes = [permissions.DjangoModelPermissions]

class RhNewDemandeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InfoDemandeSerializer
    queryset = Demande.objects.filter(approuver=None, decision=True)
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    search_fields = ['dateCongee','dureeCongee','typecongee','user','direction']
    filterset_fields = ['dateCongee','dureeCongee','typecongee','user','direction','user__first_name','user__profile__matricule']
    pagination_class = CustomPagination
    ordering_fields = ['id']
    ordering = ['id']
    permission_classes = [permissions.DjangoModelPermissions]
    

    
class CalendarViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=CalendarSerializer
    queryset=Demande.objects.filter(decision=True,approuver=True)
    permission_classes = [permissions.DjangoModelPermissions]
    
    
class LogoutView(viewsets.generics.GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CalendarEventsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset= CalendarEvents.objects.all()
    serializer_class = CalendarEventsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['direction']
    
    permission_classes = [permissions.DjangoModelPermissions]
    
    
    
@api_view(['GET'])
def get_periode(request):
    periode = Demande.objects.filter(dateCongee__range=(request.GET['debut'],request.GET['fin']),direction=request.GET['direction'],approuver=True)
    serializer = CalendarSerializer(periode,many=True)
    return Response(serializer.data)