"""
URL Configuration for api_project.

Authentication Endpoints:
- /api-token-auth/: POST username and password to obtain auth token

API Endpoints:
- /api/: Main API routes (see api/urls.py for details)
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]