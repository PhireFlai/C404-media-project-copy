from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import rest_framework

# Create your views here.
@api_view(['GET'])
def test(request):
    return Response("This is Django: Connected to Backend!")