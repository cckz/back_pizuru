from django.contrib import admin
from django.urls import path, include
from django.views import generic
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ProfileView, WorkersView

urlpatterns = [
    path('', generic.RedirectView.as_view(
        url='api/', permanent=False)),
    path('api/', get_schema_view()),
    path('api/auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    path('api/auth/token/obtain/', TokenObtainPairView.as_view()),
    path('api/auth/token/refresh/', TokenRefreshView.as_view()),
    path('api/profile/', ProfileView.as_view()),
    path('api/profile/workers/', WorkersView.as_view()),
    path('admin/', admin.site.urls),
]