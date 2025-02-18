from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics  
from .models import User, Post
from .serializers import UserSerializer, PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied


# Creates a new user
@api_view(['POST'])
def createUser(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        # Use the imported User model instead of `get_user_model()`
        admin_user = User.objects.filter(username="Admin").first()

        if not admin_user:
            admin_user = User.objects.create(username="Admin", password="defaultpassword")
        
        serializer.save(author=admin_user)  # Assign a single user instance


# Handles GET /api/posts/<id>/, PUT /api/posts/<id>/, DELETE /api/posts/<id>/
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_destroy(self, instance):
        # Temporarily allow deletion for testing only
        # needs to be changed to authenticate user 
        instance.delete()

    def perform_update(self, serializer):
        print("Request User:", self.request.user)  # Debugging
        print("Post Author:", serializer.instance.author)  # Debugging

        # Temporarily allow editing for testing
        # needs to be changed to authenticate user 
        serializer.save()
