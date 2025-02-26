from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics  
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *
import requests

@swagger_auto_schema(
    method="post",
    operation_summary="Create a new user",
    operation_description="Registers a new user with a username and password. A token is generated upon successful registration.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, 
                description="Unique username for the new user"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, 
                format=openapi.FORMAT_PASSWORD,
                description="Secure password for authentication"
            ),
        },
        required=["username", "password"],
    ),
    responses={
        201: openapi.Response(
            "User successfully created",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "token": openapi.Schema(type=openapi.TYPE_STRING, description="Authentication token for the user"),
                    "user_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Unique ID of the created user"),
                    "username": openapi.Schema(type=openapi.TYPE_STRING, description="Registered username"),
                },
            ),
        ),
        400: openapi.Response(
            "Bad Request",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message")
                },
            ),
        ),
    },
)

# Creates a new user
@api_view(['POST'])
@permission_classes([AllowAny])  # Allows anyone to sign up
def createUser(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
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
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Lists all users
@permission_classes([AllowAny])         
class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Gets all public posts
class PublicPostsView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Post.objects.filter(visibility=Post.PUBLIC)


# Gets all posts for a given user
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)  # Allow image file uploads
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get_queryset(self):
        user_id = self.kwargs.get('userId')
        if user_id:
            return Post.objects.filter(author_id=user_id).exclude(visibility=Post.DELETED)
        return Post.objects.exclude(visibility=Post.DELETED)
    
    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a post.")
        serializer.save(author=self.request.user)

# Gets, updates, or deletes a specific post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # authentication

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("You can only delete your own posts.")  
        instance.visibility = Post.DELETED
        instance.save()

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("You can only edit your own posts.")  
        serializer.save()


# Gets a user's profile or updates it
class UserProfileView(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get(self, request, userId):
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, userId):
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.id != user.id:
            return Response({'error': 'You do not have permission to update this profile'}, status=status.HTTP_403_FORBIDDEN)

        new_username = request.data.get('newUsername')
        if not new_username:
            return Response({'error': 'New username is required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=new_username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user.username = new_username
        user.save()

        return Response({'message': 'Username updated successfully'}, status=status.HTTP_200_OK)

# Updates a user's profile picture
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateUserProfile(request, userId):
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if userId != user.id:
        return Response({'error': 'You do not have permission to update this profile'}, status=status.HTTP_403_FORBIDDEN)

    profile_picture = request.FILES.get('profile_picture')
    if profile_picture:
        user.profile_picture = profile_picture
        user.save()
        return Response({'message': 'Profile picture updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No profile picture provided'}, status=status.HTTP_400_BAD_REQUEST)
    
# Creates a comment on a post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateComment(request, userId, pk):
    post = get_object_or_404(Post, id=pk)
    author = request.user
    content = request.data.get('content')
    serializer = CommentSerializer(data={'author': author.id, 'content': content, 'post': post.id})
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Posts a comment to an author's inbox
@api_view(['POST'])
@permission_classes([AllowAny])
def PostComment(request, author):
    return Response(status=status.HTTP_200_OK)

# Lists and creates comments for a specific post
class CommentsList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id)


@permission_classes([AllowAny])
class GetComment(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        id = self.kwargs['commentId']
        return Comment.objects.filter(id=id)


@permission_classes([AllowAny])
class GetCommented(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        authorID = self.kwargs['userId']
        return Comment.objects.filter(author=authorID)
    
    def perform_create(self, serializer):
        authorID = self.kwargs['userId']
        postID = self.request.data.get('post')
        content = self.request.data.get('content')
        try:
            post = Post.objects.get(id=postID)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        post_author = post.author.id
        comment_data={'author': authorID, 'content': content, 'post': postID}
        serializer = CommentSerializer(data=comment_data)
    
        if serializer.is_valid():
            serializer.save()
            comment = Comment.objects.get(id=serializer.data["id"])
            response = self.forward_to_inbox(comment, post_author)
            return response

    def forward_to_inbox(self, comment, author):
        comment_data = CommentSerializer(comment).data
        
        response = requests.post(f'http://localhost:8000/api/authors/{author}/inbox/', data=comment_data)
        return response

@permission_classes([AllowAny])
class GetCommentFromCommented(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        authorID = self.kwargs['userId']
        commentID = self.kwargs['commentId']
        return Comment.objects.filter(id=commentID, author=authorID)