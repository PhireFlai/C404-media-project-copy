from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics  
from .models import User, Post
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView


# Creates a new user
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
    
class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)  # Allow image file uploads
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get_queryset(self):
            return Post.objects.exclude(visibility=Post.DELETED)
    
    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a post.")
    
        serializer.save(author=self.request.user)
        
# Gets all post that was written by a given user and not deleted
class UserPostsView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['userId']
        return Post.objects.filter(author_id=user_id).exclude(visibility=Post.DELETED)

# Handles GET /api/posts/<id>/, PUT /api/posts/<id>/, DELETE /api/posts/<id>/
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # authentication

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            # Restrict deletion
            raise PermissionDenied("You can only delete your own posts.")  
        instance.visibility = Post.DELETED
        instance.save()

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            # Restrict editing
            raise PermissionDenied("You can only edit your own posts.")  
        serializer.save()

# Acquires a user's profile
@api_view(['GET'])
def getUserProfile(request, userId):
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # No authentication required for GET requests
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateUserProfile(request, userId):
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Ensure the authenticated user is the owner of the profile
    if userId != user.id:
        return Response({'error': 'You do not have permission to update this profile'}, status=status.HTTP_403_FORBIDDEN)

    # Update the profile picture
    profile_picture = request.FILES.get('profile_picture')
    if profile_picture:
        user.profile_picture = profile_picture
        user.save()
        return Response({'message': 'Profile picture updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No profile picture provided'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateUsername(request, userId):
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Ensure the authenticated user is the owner of the profile
    if request.user != user:
        return Response({'error': 'You do not have permission to update this profile'}, status=status.HTTP_403_FORBIDDEN)

    new_username = request.data.get('newUsername')

    if not new_username:
        return Response({'error': 'New username is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the new username is already taken
    if User.objects.filter(username=new_username).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    # Update the username
    user.username = new_username
    user.save()

    return Response({'message': 'Username updated successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def CreateComment(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    author = request.user
    content = request.data.get('content')
    serializer = CommentSerializer(data={'author': author.id, 'content': content, 'post': post.id})
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def PostComment(request, author):
    author_instance = User.objects.get(id=author)
    comment = Comment.objects.get(id=request.data.get('comment_id'))
    return Response({"message": "Comment posted to author inbox", "commentId": comment.id}, status=status.HTTP_200_OK)


class CommentsList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id)
    
    
