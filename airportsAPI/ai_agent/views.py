from django.shortcuts import render
from rest_framework.decorators import api_view

@api_view(['GET'])
def chat(req):
    return render(req, "lobby.html")
