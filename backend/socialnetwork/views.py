from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics  
from .models import User, Post
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
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


# Logs in a user
@api_view(['POST'])
def loginUser(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    print(request.data)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

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

# Acquires a user's profile or allows editing with a put request
@api_view(['GET', 'PUT'])
def getUserProfile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # No authentication required for GET requests
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        def put_view(request, user):
            if username != user.username:
                return Response({'error': 'You do not have permission to update this profile'}, status=status.HTTP_403_FORBIDDEN)

            # Update the profile picture
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                user.profile_picture = profile_picture
                user.save()
                return Response({'message': 'Profile picture updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No profile picture provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Call the nested PUT view
        return put_view(request, user)
@api_view(['POST'])
def CreateComment(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    author = request.user.id
    content = request.data.get('content')
    serializer = CommentSerializer(data={'author': author, 'content': content, 'post': post.id})
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CommentsList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id)
    
    
