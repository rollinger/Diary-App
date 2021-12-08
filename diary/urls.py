"""Diary URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    #
    # DRF
    #
    # API Base Url
    # See api_router for the routing of the viewsets
    #path("api/", include("diary.api_router")),
    # DRF Auth Token
    # POST username and password to this endpoint to get the authentication token.
    # The token is used for subsequent requests from the client.
    #path("api-auth-token/", obtain_auth_token),
]