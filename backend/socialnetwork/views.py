from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics  
from .models import User, Post
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied


# # Creates a new user
# @api_view(['POST'])
# def createUser(request):
#     print(request.data)
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()  
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])  # Allows anyone to sign up
def createUser(request):
    #print(request.data)  # Debugging purposes

    # Ensure username and password are provided
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

    # Checks if username already exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    # Create user and hash password automatically
    user = User.objects.create_user(username=username, password=password)

    # Generate token for the new user
    token = Token.objects.create(user=user)

    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    }, status=status.HTTP_201_CREATED)


# Logs in a user
@api_view(['POST'])
@permission_classes([AllowAny]) 
def loginUser(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    #print(request.data)
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
    permission_classes = [IsAuthenticated]  # Requires authentication

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a post.")
    
        serializer.save(author=self.request.user)


# Handles GET /api/posts/<id>/, PUT /api/posts/<id>/, DELETE /api/posts/<id>/
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # authentication

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            # Restrict deletion
            raise PermissionDenied("You can only delete your own posts.")  
        instance.delete()

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            # Restrict editing
            raise PermissionDenied("You can only edit your own posts.")  
        serializer.save()

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