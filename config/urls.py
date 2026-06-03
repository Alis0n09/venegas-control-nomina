from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from nomina.serializers.auth import CustomTokenView
from nomina.views.auth import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/login/',   CustomTokenView.as_view(),  name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/',  LogoutView.as_view(),        name='logout'),

    path('api/', include('nomina.urls')),
]