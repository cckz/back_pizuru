from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('account/', include('accounts.urls')),
]