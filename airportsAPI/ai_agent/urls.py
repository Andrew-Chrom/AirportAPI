from .views import chat
from django.urls import path, re_path
from . import consumers

urlpatterns = [
    path("chat/", chat)
]