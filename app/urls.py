from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from api import views
from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path, register_converter
from api.converts import DateConverter

register_converter(DateConverter, 'date')

router = routers.DefaultRouter()
router.register(r'users',views.UserViewSet,'users')
router.register(r'demandes',views.UpdateDemandeViewSet,'demandes')
router.register(r'profile',views.ProfileViewSet,'profile')
router.register(r'info-demande',views.InfoDemandeViewSet,'info-demande')
router.register(r'set-demande',views.SetDemandeViewSet,'set-demande')
router.register(r'nouvelle-demande',views.NewDemandeViewSet,'nouvelle-demande')
router.register(r'calendar',views.CalendarViewSet,'calendar')
router.register(r'rh',views.InfoRHViewSet,'rh')
router.register(r'rh-nouvelle-demande',views.RhNewDemandeViewSet,'rh-nouvelle-demande')
router.register(r'periodes',views.CalendarEventsViewSet,'periodes')
#router.register(r'logout',views.LogoutView,'logout')



urlpatterns = [
    path('admin/',admin.site.urls),
    path('api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('api/token/',views.MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refreshr'),
    path('api/logout/',views.LogoutView.as_view(),name='logout'),
    path('api/periode/',views.get_periode,name='periode'),
    path('api/',include(router.urls)),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)