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
import logging
from rest_framework.exceptions import ValidationError
from django.db.models import Q

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
    
    # Fetch the environment setting to check if admin approval is required
    setting = EnvironmentSetting.objects.first()
    if setting and setting.require_admin_approval_for_signup:
        is_approved = False  # Require admin approval
    else:
        is_approved = True  # Automatically approve

    user = User.objects.create_user(username=username, password=password, is_approved=is_approved)
    token = Token.objects.create(user=user)

    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'is_approved': user.is_approved
    }, status=status.HTTP_201_CREATED)

# Logs in a user
@api_view(['POST'])
@permission_classes([AllowAny])
def loginUser(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if not user.is_approved:
            return Response({'error': 'User is not approved by admin'}, status=status.HTTP_403_FORBIDDEN)
        
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
        return Post.objects.filter(visibility=Post.PUBLIC).order_by("-created_at") 
    
# Get all friends posts
class FriendsPostsView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the userID from the URL parameter
        user_id = self.kwargs['userId']
        user = get_object_or_404(User, id=user_id)
        # Filter posts authored by the user's friends and exclude DELETED posts
        return Post.objects.filter(
            author__in=user.friends.all()
        ).exclude(
            visibility=Post.DELETED
        ).order_by("-created_at") 

# Gets all posts for a given user
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)  # Allow image file uploads
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get_queryset(self):
        user_id = self.kwargs.get('userId')
        if user_id:
            return Post.objects.filter(author_id=user_id).exclude(visibility=Post.DELETED).order_by("-created_at")
        return Post.objects.exclude(visibility=Post.DELETED).order_by("-created_at")
    
    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a post.")
        serializer.save(author=self.request.user)

# Gets, updates, or deletes a specific post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer

    def get_permissions(self):
        """Allow any user to GET but require authentication for updates/deletes."""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Filters posts based on visibility and user authentication."""
        user = self.request.user

        queryset = Post.objects.filter(
            Q(visibility=Post.PUBLIC) | Q(visibility=Post.UNLISTED)
        )

        if user.is_authenticated:
            queryset = queryset | Post.objects.filter(
                visibility=Post.FRIENDS_ONLY, author__friends=user
            )

        return queryset

    def get_object(self):
        """Returns the post or raises 403 Forbidden if access is denied."""
        post = get_object_or_404(Post, id=self.kwargs["pk"])

        # Allow the author to view their own post
        if self.request.user == post.author:
            return post

        # If the post is friends-only but the user is not a friend, deny access
        if post.visibility == Post.FRIENDS_ONLY and self.request.user not in post.author.friends.all():
            raise PermissionDenied("You do not have permission to view this post.")

        return post

    def perform_destroy(self, instance):
        """Only the author can delete their post, otherwise raise an error."""
        if self.request.user != instance.author:
            raise PermissionDenied("You can only delete your own posts.")  
        instance.visibility = Post.DELETED
        instance.save()

    def perform_update(self, serializer):
        """Only the author can update their post."""
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("You can only edit your own posts.")
        
        # Handle image updates
        image = self.request.FILES.get('image')
        if image:
            serializer.save(image=image)
        else:
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
    data={'content': content, 'post': post.id}
    serializer = CommentSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save(author=author)
        comment = Comment.objects.get(id=serializer.data['id'])
        response = requests.post(f'http://localhost:8000/api/authors/{userId}/inbox/', data=CommentSerializer(comment).data)
        return Response(serializer.data, status=response.status_code)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Post to an author's inbox
@api_view(['POST'])
@permission_classes([AllowAny])
def PostToInbox(request, receiver):
    return Response({"message": "Request received"}, status=status.HTTP_200_OK)

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
        author = User.objects.get(id=authorID)
        postID = self.request.data.get('post')
        content = self.request.data.get('content')
        try:
            post = Post.objects.get(id=postID)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        post_author = post.author.id
        comment_data={'content': content, 'post': postID}
        serializer = CommentSerializer(data=comment_data)
    
        if serializer.is_valid():
            serializer.save(author=author)
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
    
@permission_classes([AllowAny])
class FollowRequestListView(generics.ListCreateAPIView):
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestSerializer

    def get_queryset(self):
        objectId = self.kwargs['objectId']
        return FollowRequest.objects.filter(object=objectId)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def CreateFollowRequest(request, actorId, objectId):
    actor = User.objects.get(id=actorId)
    object = User.objects.get(id=objectId)
    if FollowRequest.objects.filter(actor=actorId, object=objectId).exists():
        return Response({"message": "Follow request has already been sent"}, status=status.HTTP_400_BAD_REQUEST)    
    elif actor.following.filter(id=objectId).exists():
        return Response({"message": "You are already following this user"}, status=status.HTTP_400_BAD_REQUEST)
    summary = f'{actor.username} wants to follow {object.username}'
    data = {"summary": summary}
    serializer = FollowRequestSerializer(data=data)
    if serializer.is_valid():
        serializer.save(actor=actor, object=object)
        request = FollowRequest.objects.get(actor=actor, object=object)
        request_data = FollowRequestSerializer(request).data
        response = requests.post(f'http://localhost:8000/api/authors/{object.id}/inbox/', data=request_data)
        return Response(serializer.data, status=response.status_code)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def AcceptFollowRequest(request, objectId, actorId ):
    try:
        follow_request = FollowRequest.objects.get(actor=actorId, object=objectId)
    except FollowRequest.DoesNotExist:
        return Response({'error': 'Follow request not found'}, status=status.HTTP_404_NOT_FOUND)

    if objectId != request.user.id:
        return Response({'error': 'You are not authorized to accept this request'}, 
                       status=status.HTTP_403_FORBIDDEN)

    action = request.query_params.get('action', '').lower()
    
    if action not in ['accept', 'reject']:
        return Response({'error': 'Invalid action. Please use "accept" or "reject"'},
                       status=status.HTTP_400_BAD_REQUEST)

    if action == 'accept':
        # Add the follower, if they are mututally following, add each other as friends
        follow_request.object.followers.add(follow_request.actor)
        if(follow_request.actor.followers.filter(id=follow_request.object.id).exists() == True):
            follow_request.actor.friends.add(follow_request.object)
            follow_request.object.friends.add(follow_request.actor)
        message = 'Follow request accepted successfully'
    else:
        # Reject the request
        message = 'Follow request rejected successfully'

    # Delete the follow request
    follow_request.delete()
    
    return Response({
        'message': message,
    }, status=status.HTTP_200_OK)
    
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Unfollow(request, followedId, followerId):
    try:
        followed = User.objects.get(id=followedId)
        follower = User.objects.get(id=followerId)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if follower.id != request.user.id:
        return Response({'error': 'You are not authorized to unfollow this user'}, 
                       status=status.HTTP_403_FORBIDDEN)

    
    # Unfollow the user
    followed.followers.remove(follower)
    
    if follower in followed.friends.all():
        # Remove each other as friends
        followed.friends.remove(follower)
        follower.friends.remove(followed)
    return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def RemoveFollower(request, followerId, followedId):
    try:
        followed = User.objects.get(id=followedId)
        follower = User.objects.get(id=followerId)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if followed.id != request.user.id:
        return Response({'error': 'You are not authorized to remove this follower'}, 
                       status=status.HTTP_403_FORBIDDEN)

    # Remove the follower
    followed.followers.remove(follower)
    
    if followed in follower.friends.all():
        # Remove each other as friends
        followed.friends.remove(follower)
        follower.friends.remove(followed)
    
    return Response({'message': 'Follower removed successfully'}, status=status.HTTP_200_OK)    
    
@permission_classes([AllowAny])
class FollowersList(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        userId = self.kwargs['userId']
        user = get_object_or_404(User, id=userId)
        return user.followers.all()
    
@permission_classes([AllowAny])
class FollowingList(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        userId = self.kwargs['userId']
        user = get_object_or_404(User, id=userId)
        return user.following.all()

# Add a like on a post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddLike(request, userId, pk):
    post = get_object_or_404(Post, id=pk)
    user = request.user
    data = {'post': post.id}
    serializer = LikeSerializer(data=data)

    if serializer.is_valid():
        serializer.save(user=user)
        like = Like.objects.get(id=serializer.data['id'])
        response = requests.post(f'http://localhost:8000/api/authors/{userId}/inbox/', data=LikeSerializer(like).data)
        return Response(serializer.data, status=response.status_code)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikesList(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Like.objects.filter(post_id=post_id)
    
@permission_classes([AllowAny])
class GetLiked(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        authorID = self.kwargs['userId']
        return Like.objects.filter(user=authorID)
    
    def perform_create(self, serializer):
        authorID = self.kwargs['userId']
        author = User.objects.get(id=authorID)
        postID = self.request.data.get('post')
        try:
            post = Post.objects.get(id=postID)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        post_author = post.author.id
        like_data = {'post': postID}
        serializer = LikeSerializer(data=like_data)
    
        if serializer.is_valid():
            serializer.save(user=author)
            like = Like.objects.get(id=serializer.data["id"])
            response = self.forward_to_inbox(like, post_author)
            return response

    def forward_to_inbox(self, like, author):
        like_data = LikeSerializer(like).data
        
        response = requests.post(f'http://localhost:8000/api/authors/{author}/inbox/', data=like_data)
        return response

@permission_classes([AllowAny])
class GetSingleLike(generics.RetrieveAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = 'id'

    def get_queryset(self):
        likeID = self.kwargs['id']
        return Like.objects.filter(id=likeID)

@permission_classes([AllowAny])
class GetLikesByAuthor(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        authorID = self.kwargs['authorId']
        return Like.objects.filter(user=authorID)

# Add a like on a comment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddCommentLike(request, userId, pk, ck):
    comment = get_object_or_404(Comment, id=ck)
    user = request.user
    data = {'comment': comment.id}
    serializer = CommentLikeSerializer(data=data)

    if serializer.is_valid():
        serializer.save(user=user)
        like = CommentLike.objects.get(id=serializer.data['id'])
        response = requests.post(f'http://localhost:8000/api/authors/{userId}/inbox/', data=CommentLikeSerializer(like).data)
        return Response(serializer.data, status=response.status_code)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentLikesList(generics.ListCreateAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer

    def get_queryset(self):
        comment_id = self.kwargs['ck']
        return CommentLike.objects.filter(comment_id=comment_id)
    
class UserFeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Fetches the authenticated user's feed, ensuring the user sees:
        - Their own posts (excluding deleted ones).
        - Public posts from any author.
        - Friends-only posts if the author is a friend.
        - Unlisted posts if the author is a friend or follower.
        """
        
        user = self.request.user

        if not user.is_authenticated:
            # Return only public posts if the user is not authenticated
            return Post.objects.filter(visibility=Post.PUBLIC).exclude(visibility=Post.DELETED).order_by("-updated_at")

        # Extract only the IDs of friends and followers
        friend_ids = user.friends.values_list('id', flat=True)  # Extract only the 'id' field
        following_ids = user.following.values_list('id', flat=True) # Changed follower to following

        return Post.objects.filter(
            Q(author=user) |  # Show ALL posts by the user (excluding deleted)
            Q(visibility=Post.PUBLIC) |
            Q(visibility=Post.FRIENDS_ONLY, author__in=friend_ids) |
            Q(visibility=Post.UNLISTED, author__in=friend_ids) |  # Unlisted for friends
            Q(visibility=Post.UNLISTED, author__in=following_ids)  # Unlisted for followers
        ).exclude(
            visibility=Post.DELETED
        ).order_by("-updated_at")  # Show latest posts first