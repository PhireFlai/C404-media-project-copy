from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics  
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *
import requests
from django.db.models import Q
from django.http import JsonResponse
from socialnetwork.permissions import IPLockPermission, MultiAuthPermission, ConditionalMultiAuthPermission
from .utils import forward_get_request
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse
from django.test import RequestFactory


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
@permission_classes([AllowAny])  # Allows anyone to sign up locally
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
class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [MultiAuthPermission]
    
# Get all friends posts
class FriendsPostsView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [MultiAuthPermission]

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
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]  

    def get_queryset(self):
        user_id = self.kwargs.get('userId')  # Extract userId from URL
        viewer = self.request.user  # The logged-in user

        author = get_object_or_404(User, id=user_id)  # Fetch the profile owner

        if not viewer.is_authenticated:
            return Post.objects.filter(author=author, visibility=Post.PUBLIC).order_by("-updated_at")

        author = get_object_or_404(User, id=user_id)  # Fetch the profile owner

        # Check if viewer follows the author
        viewer_follows_author = viewer in author.followers.all()
        author_follows_viewer = author in viewer.followers.all()
        mutual_follow = viewer_follows_author and author_follows_viewer

        # Fetch posts based on visibility ranking
        if viewer == author:
            # If the viewer is the profile owner, show all their posts
            return Post.objects.filter(author=author).exclude(visibility=Post.DELETED).order_by("-updated_at")
        elif mutual_follow:
            # If the viewer and author follow each other, show public, friends-only, and unlisted posts
            return Post.objects.filter(author=author).exclude(visibility=Post.DELETED).order_by("-updated_at")
        elif viewer_follows_author:
            # If the viewer follows the author, show public + unlisted posts (but NOT friends-only)
            return Post.objects.filter(author=author, visibility__in=[Post.PUBLIC, Post.UNLISTED]).exclude(visibility=Post.DELETED).order_by("-created_at")
        else:
            # If no relationship, only show public posts
            return Post.objects.filter(author=author, visibility=Post.PUBLIC).exclude(visibility=Post.DELETED).order_by("-created_at")


    
    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a post.")
        post = serializer.save(author=self.request.user)
        
        # Fetch followers with remote_fqid
        followers_with_remote_fqid = self.request.user.followers.filter(remote_fqid__isnull=False)
        # print(followers_with_remote_fqid)
        # Send the post to each follower's inbox
        for follower in followers_with_remote_fqid:
            
            parsed_url = follower.remote_fqid.split('/')
            remote_domain_base = parsed_url[2]

            # Remove the port from the remote domain
            print(parsed_url)
            print(remote_domain_base)
            parsed_remote_url = urlparse(f"http://{remote_domain_base}")
            remote_domain_without_brackets = parsed_remote_url.hostname  # Extract the hostname without the port
            remote_domain = f"[{remote_domain_without_brackets}]"  # Add brackets for IPv6 format

            
            try:
                remote_node = RemoteNode.objects.get(url=f"http://{remote_domain}/")
                auth = HTTPBasicAuth(remote_node.username, remote_node.password)
            except RemoteNode.DoesNotExist:
                return Response({'error': 'Remote node not configured'}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
            inbox_url = f"{follower.remote_fqid}inbox/"
            post_data = PostSerializer(post).data
            post_data.update({'remote_fqid' : post_data['id']})
            print(post_data)
            headers = {"Content-Type": "application/json"}
            
            try:
                print(inbox_url)
                response = requests.post(inbox_url, auth = auth, json=post_data, headers=headers)
                print(response.json())
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Failed to send post to {follower.username}'s inbox: {e}")


# Gets, updates, or deletes a specific post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer

    def get_permissions(self):
        """Allow any user to GET but require authentication for updates/deletes."""
        if self.request.method == 'GET':
            return [AllowAny()]  # Instantiate the AllowAny class
        return [MultiAuthPermission()]  # Instantiate the MultiAuthPermission class

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
        post = instance
        instance.save()
        
                
        # Fetch followers with remote_fqid
        followers_with_remote_fqid = self.request.user.followers.filter(remote_fqid__isnull=False)
        # print(followers_with_remote_fqid)
        # Send the post to each follower's inbox
        for follower in followers_with_remote_fqid:
            
            parsed_url = follower.remote_fqid.split('/')
            remote_domain_base = parsed_url[2]

            # Remove the port from the remote domain
            parsed_remote_url = urlparse(f"http://{remote_domain_base}")
            remote_domain_without_brackets = parsed_remote_url.hostname  # Extract the hostname without the port
            remote_domain = f"[{remote_domain_without_brackets}]"  # Add brackets for IPv6 format

            
            try:
                remote_node = RemoteNode.objects.get(url=f"http://{remote_domain}/")
                auth = HTTPBasicAuth(remote_node.username, remote_node.password)
            except RemoteNode.DoesNotExist:
                return Response({'error': 'Remote node not configured'}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
            inbox_url = f"{follower.remote_fqid}inbox/"
            post_data = PostSerializer(post).data
            post_data.update({'remote_fqid' : post_data['id']})

            headers = {"Content-Type": "application/json"}
            
            try:
                print(inbox_url)
                response = requests.post(inbox_url, auth = auth, json=post_data, headers=headers)
                print(response.json())
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Failed to send post to {follower.username}'s inbox: {e}")

    def perform_update(self, serializer):
        """Only the author can update their post."""
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("You can only edit your own posts.")
        
        
        # Handle image updates
        image = self.request.FILES.get('image')
        if image:
            post = serializer.save(image=image)
        else:
            post = serializer.save()
        
        # Fetch followers with remote_fqid
        followers_with_remote_fqid = self.request.user.followers.filter(remote_fqid__isnull=False)
        # print(followers_with_remote_fqid)
        # Send the post to each follower's inbox
        for follower in followers_with_remote_fqid:
            
            parsed_url = follower.remote_fqid.split('/')
            remote_domain_base = parsed_url[2]

            # Remove the port from the remote domain
            parsed_remote_url = urlparse(f"http://{remote_domain_base}")
            remote_domain_without_brackets = parsed_remote_url.hostname  # Extract the hostname without the port
            remote_domain = f"[{remote_domain_without_brackets}]"  # Add brackets for IPv6 format

            
            try:
                remote_node = RemoteNode.objects.get(url=f"http://{remote_domain}/")
                auth = HTTPBasicAuth(remote_node.username, remote_node.password)
            except RemoteNode.DoesNotExist:
                return Response({'error': 'Remote node not configured'}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
            inbox_url = f"{follower.remote_fqid}inbox/"
            post_data = PostSerializer(post).data
            post_data.update({'remote_fqid' : post_data['id']})
            print(post_data)
            headers = {"Content-Type": "application/json"}
            
            try:
                print(inbox_url)
                response = requests.post(inbox_url, auth = auth, json=post_data, headers=headers)
                print(response.json())
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Failed to send post to {follower.username}'s inbox: {e}")

# Gets a user's profile or updates it
class UserProfileView(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT':
            self.permission_classes = [MultiAuthPermission]
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
@permission_classes([MultiAuthPermission])
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
@permission_classes([MultiAuthPermission])
def CreateComment(request, userId, pk):
    post = get_object_or_404(Post, id=pk)
    author = request.user
    content = request.data.get('content')
    
    # Create comment and update post timestamp
    comment = Comment.objects.create(
        author=author,
        post=post, 
        content=content
    )
    
    # Serialize both comment and updated post
    comment_serializer = CommentSerializer(comment)

    # Get followers with remote_fqid - identical to perform_update
    followers_with_remote_fqid = post.author.followers.filter(remote_fqid__isnull=False)
    
    for follower in followers_with_remote_fqid:
            
        parsed_url = follower.remote_fqid.split('/')
        remote_domain_base = parsed_url[2]

        # Remove the port from the remote domain
        parsed_remote_url = urlparse(f"http://{remote_domain_base}")
        remote_domain_without_brackets = parsed_remote_url.hostname  # Extract the hostname without the port
        remote_domain = f"[{remote_domain_without_brackets}]"  # Add brackets for IPv6 format
        
        try:
            remote_node = RemoteNode.objects.get(url=f"http://{remote_domain}/")
            auth = HTTPBasicAuth(remote_node.username, remote_node.password)
        except RemoteNode.DoesNotExist:
            return Response({'error': 'Remote node not configured'}, 
                      status=status.HTTP_400_BAD_REQUEST)
        
        inbox_url = f"{follower.remote_fqid}inbox/"
        comment_data = CommentSerializer(comment).data
        comment_data.update({'remote_fqid' : comment_data['id']})
        print(comment_data)
        headers = {"Content-Type": "application/json"}
        
        try:
            print(inbox_url)
            response = requests.post(inbox_url, auth = auth, json=comment_data, headers=headers)
            print(response.json())
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to send post to {follower.username}'s inbox: {e}")
        # Send to post author's inbox if they're remote
    if post.author.remote_fqid:
        try:
            remote_node_fqid = extract_ipv6_address(post.author.remote_fqid)

            remote_node = RemoteNode.objects.get(url=remote_node_fqid)
            auth = HTTPBasicAuth(remote_node.username, remote_node.password)
            
            comment_data = CommentSerializer(comment).data
            print(post.author.remote_fqid)
            author_inbox_url = f"{post.author.remote_fqid}inbox/"
            response = requests.post(
                author_inbox_url,
                auth=auth,
                json=comment_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to send to post author: {str(e)}")
    
    return Response(comment_serializer.data, status=status.HTTP_201_CREATED)

# Post to an author's inbox
@api_view(["POST"])
@permission_classes([AllowAny])
def IncomingPostToInbox(request, receiver):
    try:
        type = request.data.get("type")

        if type == "follow":
            summary = request.data.get("summary")
            actor = request.data.get("actor")
            object = request.data.get("object")
            actor_id = actor['id'].split('/')[-2]
            object_id = object['id'].split('/')[-2]


            # Get or create the actor and object users
            actor_obj, created_actor = User.objects.get_or_create(
                id=actor_id,
                defaults={
                    "remote_fqid": actor['id'],
                    "username": actor.get('username'),
                }
            )
            object_obj, created_object = User.objects.get_or_create(
                id=object_id,
                defaults={
                    "remote_fqid": object['id'],
                    "username": object.get('username'),
                }
            )

            # Check if the follow request already exists
            if FollowRequest.objects.filter(actor=actor_obj, object=object_obj).exists():
                return Response({"message": "Follow request has already been sent"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the actor is already following the object
            if actor_obj.following.filter(id=object_obj.id).exists():
                return Response({"message": "You are already following this user"}, status=status.HTTP_400_BAD_REQUEST)

            # Manually create the FollowRequest object
            follow_request = FollowRequest.objects.create(
                summary=summary,
                actor=actor_obj,
                object=object_obj
            )

            # Return the created FollowRequest data
            return Response({
                "id": follow_request.id,
                "type": follow_request.type,
                "summary": follow_request.summary,
                "actor": {
                    "id": actor_obj.id,
                    "username": actor_obj.username,
                },
                "object": {
                    "id": object_obj.id,
                    "username": object_obj.username,
                }
            }, status=status.HTTP_201_CREATED)

        elif type == "accept_follow":
            print("Accepting follow request")
            print(request.data)

            actor = request.data.get("actor")
            object = request.data.get("object")
            actor_id = actor['id']
            object_id = object['id']

            print(f"Actor: {actor}\n Object: {object}\n Actor_Id: {actor_id}\nObject_Id: {object_id}")

            try:
                # Fetch the follow request
                follow_request = FollowRequest.objects.get(actor_id=actor_id, object_id=object_id)
                print(f"Got the follow request from the database")
            except FollowRequest.DoesNotExist:
                return Response({'error': 'Follow request not found'}, status=status.HTTP_404_NOT_FOUND)

            # Add the actor to the object's followers
            follow_request.object.followers.add(follow_request.actor)

            # If they are mutually following, add each other as friends
            if follow_request.actor.followers.filter(id=follow_request.object.id).exists():
                follow_request.actor.friends.add(follow_request.object)
                follow_request.object.friends.add(follow_request.actor)

            # Delete the follow request after accepting
            follow_request.delete()

            return Response({"message": "Follow request accepted successfully"}, status=status.HTTP_200_OK)

        elif type == "delete_follow_request":
            print("Deleting follow request")
            print(request.data)

            actor = request.data.get("actor")
            object = request.data.get("object")
            actor_id = actor['id'].split('/')[-2]
            object_id = object['id'].split('/')[-2]

            try:
                # Fetch the follow request
                follow_request = FollowRequest.objects.get(actor_id=actor_id, object_id=object_id)
                follow_request.delete()
                return Response({"message": "Follow request deleted successfully"}, status=status.HTTP_200_OK)
            except FollowRequest.DoesNotExist:
                return Response({'error': 'Follow request not found'}, status=status.HTTP_404_NOT_FOUND)

        elif type == "comment":
            comment_data = request.data
            print("Processing comment:", comment_data)

            # Extract comment ID from URL
            comment_id = comment_data.get("id").rstrip('/').split('/')[-1]
            
            # Extract author data
            author_data = comment_data.get("author")
            author_id = author_data.get("id").rstrip('/').split('/')[-1]

            # Extract post data from comment's post field
            post_url = comment_data.get("post")
            url_parts = post_url.rstrip('/').split('/')
            
            try:
                # Find the index of 'posts' in the URL path
                posts_index = url_parts.index('posts')
                post_id = url_parts[posts_index + 1]
                
                # Find the index of 'authors' to get post author ID
                authors_index = url_parts.index('authors')
                post_author_id = url_parts[authors_index + 1]
                
            except (ValueError, IndexError) as e:
                return Response(
                    {"error": f"Invalid post URL structure: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get or create comment author
            author_obj, _ = User.objects.get_or_create(
                id=author_id,
                defaults={
                    "username": author_data.get("username"),
                    "email": author_data.get("email"),
                    "profile_picture": author_data.get("profile_picture"),
                    "remote_fqid": author_data.get("id")
                }
            )

            # Get or create parent post
    # Get existing post (DO NOT CREATE NEW ONE)
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return Response(
                    {"error": f"Linked post {post_id} does not exist locally"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Rest of the code remains the same...
            # Create/update comment
            comment, created = Comment.objects.update_or_create(
                id=comment_id,
                defaults={
                    "author": author_obj,
                    "content": comment_data.get("content"),
                    "post": post,  # Now properly linked to valid post
                    "created_at": comment_data.get("created_at") or timezone.now(),
                    "type": comment_data.get("type", "comment")
                }
            )

            # Process likes
            for like_data in comment_data.get("likes", []):
                like_author_data = like_data.get("author")
                like_author_id = like_author_data.get("id").rstrip('/').split('/')[-1]

                like_author, _ = User.objects.get_or_create(
                    id=like_author_id,
                    defaults={
                        "username": like_author_data.get("username"),
                        "remote_fqid": like_author_data.get("id")
                    }
                )

                Like.objects.update_or_create(
                    id=like_data.get("id"),
                    defaults={
                        "author": like_author,
                        "content_object": comment,
                        "created_at": like_data.get("published") or timezone.now()
                    }
                )

            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        
        elif type == "post":
            print("POST")
            print(request.data)
            post_data = request.data

            # Extract post ID from URL
            post_id = post_data.get("id").rstrip('/').split('/')[-1]
            
            # Extract author data
            author_data = post_data.get("author")
            author_id = author_data.get("id").rstrip('/').split('/')[-1]

            # Get or create author
            author_obj, _ = User.objects.get_or_create(
                id=author_id,
                defaults={
                    "username": author_data.get("username"),
                    "email": author_data.get("email"),
                    "profile_picture": author_data.get("profile_picture"),
                    "remote_fqid": author_data.get("id")
                }
            )

            # Handle post timestamps
            created_at = post_data.get("created_at") 
            updated_at = post_data.get("updated_at") 

            # Create/update post
            post, _ = Post.objects.update_or_create(
                id=post_id,
                defaults={
                    "title": post_data.get("title"),
                    "content": post_data.get("content"),
                    "author": author_obj,
                    "visibility": post_data.get("visibility"),
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "remote_fqid": post_data.get("id")
                }
            )

            # Handle comments
            for comment_data in post_data.get("comments", []):
                comment_id = comment_data["id"].rstrip('/').split('/')[-1]
                comment_author_data = comment_data["author"]
                comment_author_id = comment_author_data["id"].rstrip('/').split('/')[-1]

                # Get or create comment author
                comment_author, _ = User.objects.get_or_create(
                    id=comment_author_id,
                    defaults={
                        "username": comment_author_data.get("username"),
                        "email": comment_author_data.get("email"),
                        "profile_picture": comment_author_data.get("profile_picture"),
                        "remote_fqid": comment_author_data.get("id")
                    }
                )

                # Create/update comment
                Comment.objects.update_or_create(
                    id=comment_id,
                    defaults={
                        "author": comment_author,
                        "content": comment_data["content"],
                        "post": post,
                        "created_at": comment_data.get("created_at"),
                        "type": comment_data.get("type", "comment")
                    }
                )

            # Return complete post data
            return Response({
                "id": f"http://[{my_ip}]:8000/api/authors/{post.author.id}/posts/{post.id}/",
                "author": UserSerializer(post.author).data,
                "title": post.title,
                "content": post.content,
                "image": post.image.url if post.image else None,
                "formatted_content": markdown.markdown(post.content),
                "created_at": post.created_at,
                "updated_at": post.updated_at,
                "visibility": post.visibility,
                "like_count": post.like_count,
                "type": "post",
                "remote_fqid": post.remote_fqid,
                "comments": CommentSerializer(post.comments.all(), many=True).data
            }, status=status.HTTP_201_CREATED)
        
        elif type == "like":
            author = request.data.get("author")
            author_id = author['id'].rstrip('/').split('/')[-1]
            created_at = request.data.get("created_at")
            id = request.data.get("id")
            post = request.data.get("post")
            author_obj, created_author = User.objects.get_or_create(id=author_id, remote_fqid=author['id'])
            data={
                "created_at": created_at,
                "id": id,
                "post": post,
            }
            serializer = LikeSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=author_obj)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Unsupported message type"}, status=status.HTTP_400_BAD_REQUEST)


class IsFriendOrAuthor(BasePermission):
    def has_permission(self, request, view):
        post_id = view.kwargs.get('pk')
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        if post.visibility == Post.PUBLIC:
            return True
        elif post.visibility == Post.FRIENDS_ONLY:
            return user in post.author.friends.all() or user == post.author
        elif post.visibility == Post.UNLISTED:
            return user in post.author.followers.all() or user == post.author
        return False

class IsCommentAuthorOrPostAuthorOrFriend(BasePermission):
    def has_permission(self, request, view):
        comment_id = view.kwargs.get('commentId')
        comment = get_object_or_404(Comment, id=comment_id)
        post = comment.post
        user = request.user

        if post.visibility == Post.PUBLIC:
            return True
        if post.visibility == Post.FRIENDS_ONLY:
            return user in post.author.friends.all() or user == post.author or user == comment.author
        elif post.visibility == Post.UNLISTED:
            return user in post.author.followers.all() or user == post.author or user == comment.author
        return False

@permission_classes([IsFriendOrAuthor])
class CommentsList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id)

@permission_classes([IsCommentAuthorOrPostAuthorOrFriend])
# @permission_classes([AllowAny])
class GetComment(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        id = self.kwargs['commentId']
        return Comment.objects.filter(id=id)

class GetCommented(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [ConditionalMultiAuthPermission]

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
        factory = RequestFactory()
        request = factory.post(f'http://backend:8000/api/authors/{author}/inbox/', data=comment_data)
        response = IncomingPostToInbox(request, author)
        return response

class GetCommentFromCommented(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [ConditionalMultiAuthPermission]

    def get_queryset(self):
        authorID = self.kwargs['userId']
        commentID = self.kwargs['commentId']
        return Comment.objects.filter(id=commentID, author=authorID)
    
class FollowRequestListView(generics.ListCreateAPIView):
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestSerializer
    permission_classes = [ConditionalMultiAuthPermission]

    def get_queryset(self):
        objectId = self.kwargs['objectId']
        return FollowRequest.objects.filter(object=objectId)
    
@api_view(['POST'])
@permission_classes([ConditionalMultiAuthPermission])
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
        factory = RequestFactory()
        request = factory.post(f'http://localhost:8000/api/authors/{object.id}/inbox/', data=request_data)
        response = IncomingPostToInbox(request, object.id)
        return Response(serializer.data, status=response.status_code)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def createForeignFollowRequest(request, actorId, objectFQID):
    actor = User.objects.get(id=actorId)
        
    # Parse the foreign author's FQID (Fully Qualified ID)
    parsed_url = objectFQID.strip('/').split('/')
    remote_domain_base = parsed_url[1]
    print(parsed_url)
    author_path_with_port = '/'.join(parsed_url[2:])
    print("author path with port ", author_path_with_port)
    port_removed_path = author_path_with_port
    print("port removed path ", port_removed_path)

    # Remove the port from the remote domain
    parsed_remote_url = urlparse(f"http://{remote_domain_base}")
    remote_domain_without_brackets = parsed_remote_url.hostname  # Extract the hostname without the port
    remote_domain = f"[{remote_domain_without_brackets}]"  # Add brackets for IPv6 format

    author_path =  f"http://{remote_domain}/{port_removed_path}"

    print("remote domain ", remote_domain)
    print("author path ", author_path)
    
    try:
        remote_node = RemoteNode.objects.get(url=f"http://{remote_domain}/")
        auth = HTTPBasicAuth(remote_node.username, remote_node.password)
    except RemoteNode.DoesNotExist:
        return Response({'error': 'Remote node not configured'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    try:
        response = requests.get(
                author_path,  # Use IPv6 format
                auth=auth,
                timeout=5
        )
        response.raise_for_status()
        remote_author = response.json()
        # return response
    except requests.exceptions.RequestException as e:
        return Response({'error': f'Failed to fetch remote author: {str(e)}'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        # Create local follow request
    if FollowRequest.objects.filter(actor=actor, object__remote_fqid=objectFQID).exists():
        return Response({"message": "Follow request already sent"},
                        status=status.HTTP_400_BAD_REQUEST)
    
    remote_fqid = remote_author.get('id')
    remote_id = remote_fqid.split('/')[-2]
    user_data = {
        "id": remote_id,  # Assuming 'id' is the key for the unique identifier
        "remote_fqid": objectFQID,
        "username": remote_author.get('username'),
    }

    print(remote_id)
    print("user data ", user_data)
    print(remote_author)
    summary = f'{actor.username} wants to follow {remote_author.get("username")}'
    if (User.objects.filter(id=remote_id).exists()):
        copy_remote = User.objects.get(id=remote_id)
    else:
        copy_remote = User.objects.create(**user_data)
    data = {"summary": summary}
    
    serializer = FollowRequestSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save(actor=actor, object=copy_remote)
        request = FollowRequest.objects.get(actor=actor, object=copy_remote)
        request_data = FollowRequestSerializer(request).data
        print(request_data)
        headers = {"Content-Type": "application/json"}
        response = requests.post(f'http://{remote_domain}/api/authors/{remote_id}/inbox/', json=request_data, headers=headers, auth=auth)
         # Return the response content and status code
        try:
            response.raise_for_status()  # Raise an exception for HTTP errors
            return Response(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            # Handle errors and return the error message
            return Response(
                {"error": str(e), "details": response.text},
                status=response.status_code
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    




@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([MultiAuthPermission])
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

    # Handle local side
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

    # Handle remote side, if applicable
    if follow_request.actor.remote_fqid:
        try:
            parsed_url = follow_request.actor.remote_fqid.split('/')
            remote_domain_base = parsed_url[2]

            # Remove the port from the remote domain
            parsed_remote_url = urlparse(f"http://{remote_domain_base}")
            remote_domain_without_brackets = parsed_remote_url.hostname  # Extract the hostname without the port
            remote_domain = f"[{remote_domain_without_brackets}]"  # Add brackets for IPv6 format

            remote_node = RemoteNode.objects.get(url=f"http://{remote_domain}/")
            auth = HTTPBasicAuth(remote_node.username, remote_node.password)

            object_remote_fqid_base = RemoteNode.objects.get(is_my_node=True).url
            object_remote_fqid = f"{object_remote_fqid_base}authors/{follow_request.object.id}/"

            # Determine the action (accept or reject)
            if action == 'accept':
                follow_data = {
                    "type": "accept_follow",
                    "summary": f"{follow_request.actor.username}'s follow request to {follow_request.object.username} was accepted",
                    "actor": {
                        "id": str(follow_request.actor.id),
                        "username": follow_request.actor.username,
                        "remote_fqid": object_remote_fqid,
                    },
                    "object": {
                        "id": str(follow_request.object.id),
                        "username": follow_request.object.username,
                        "remote_fqid": follow_request.object.remote_fqid,
                    },
                }
            elif action == 'reject':
                follow_data = {
                    "type": "decline_follow",
                    "summary": f"{follow_request.actor.username}'s follow request to {follow_request.object.username} was rejected",
                    "actor": {
                        "id": str(follow_request.actor.id),
                        "username": follow_request.actor.username,
                        "remote_fqid": object_remote_fqid,
                    },
                    "object": {
                        "id": str(follow_request.object.id),
                        "username": follow_request.object.username,
                        "remote_fqid": follow_request.object.remote_fqid,
                    },
                }

            author_inbox_url = f"{follow_request.actor.remote_fqid}inbox/"
            response = requests.post(
                author_inbox_url,
                auth=auth,
                json=follow_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
        except Exception as e:
            return Response({'error': f'Failed to send {action}_follow request: {str(e)}'},
                            status=status.HTTP_400_BAD_REQUEST)
    
    # Delete the follow request
    follow_request.delete()
    
    return Response({
        'message': message,
    }, status=status.HTTP_200_OK)
    
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([MultiAuthPermission])
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
@permission_classes([MultiAuthPermission])
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
    
class FollowersList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [ConditionalMultiAuthPermission]

    def get_queryset(self):
        userId = self.kwargs['userId']
        user = get_object_or_404(User, id=userId)
        return user.followers.all()
    
class FollowingList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [ConditionalMultiAuthPermission]

    def get_queryset(self):
        userId = self.kwargs['userId']
        user = get_object_or_404(User, id=userId)
        return user.following.all()


class FriendsList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [ConditionalMultiAuthPermission]

    def get_queryset(self):
        userId = self.kwargs['userId']
        user = get_object_or_404(User, id=userId)
        return user.friends.all()
    

# Add a like on a post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddLikeOnPost(request, userId, object_id):
    user = request.user
    post = get_object_or_404(Post, id=object_id)

    # Check if the user has already liked the post
    if Like.objects.filter(user=user, object_id=post.id, content_type=ContentType.objects.get_for_model(Post)).exists():
        return Response({'error': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the Like object
    content_type = ContentType.objects.get_for_model(Post)
    data = {'user': user.id, 'content_type': content_type.id, 'object_id': post.id}
    like = Like.objects.create(user=user, content_type=content_type, object_id=post.id)

    # Forward the like to the inbox (if this functionality exists)
    inbox_url = f"http://backend:8000/api/authors/{userId}/inbox/"

    serializer = LikeSerializer(data=data)

    if serializer.is_valid():
        serializer.save(user=user)
        like_id = serializer.data['id'].strip('/').split('/')[-1]
        like = Like.objects.get(id=like_id)
    
    factory = RequestFactory()
    request = factory.post(inbox_url, data=LikeSerializer(like).data)
    IncomingPostToInbox(request, userId)
    return Response(LikeSerializer(like).data, status=status.HTTP_200_OK)

class LikesList(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [ConditionalMultiAuthPermission]

    def get_queryset(self):
        object_id = self.kwargs['object_id']
        return Like.objects.filter(object_id=object_id)
    
class GetLiked(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [ConditionalMultiAuthPermission]

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
        
        # response = requests.post(f'http://backend:8000/api/authors/{author}/inbox/', data=like_data)
        factory = RequestFactory()
        request = factory.post(f'http://backend:8000/api/authors/{author}/inbox/', data=like_data)
        response = IncomingPostToInbox(request, author)
        return response

# Get a single like by id
class GetSingleLike(generics.RetrieveAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [ConditionalMultiAuthPermission]
    lookup_field = 'id'

    def get_queryset(self):
        likeID = self.kwargs['id']
        return Like.objects.filter(id=likeID)

# Get likes by author
class GetLikesByAuthor(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [ConditionalMultiAuthPermission]

    def get_queryset(self):
        authorID = self.kwargs['authorId']
        return Like.objects.filter(user=authorID)

# Get likes by post
@permission_classes([ConditionalMultiAuthPermission])
class GetPostLikes(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [ConditionalMultiAuthPermission]

    def get_queryset(self):
        postID = self.kwargs['postId']
        return Like.objects.filter(object_id=postID)

# Add a like on a comment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddCommentLike(request, userId, pk, ck):
    user = request.user

    # Fetch the comment based on the comment ID (ck)
    comment = get_object_or_404(Comment, id=ck)

    # Check if the user has already liked the comment
    if Like.objects.filter(user=user, object_id=comment.id, content_type=ContentType.objects.get_for_model(Comment)).exists():
        return Response({'error': 'You have already liked this comment.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the Like object
    content_type = ContentType.objects.get_for_model(Comment)
    data = {'user': user.id, 'content_type': content_type.id, 'object_id': comment.id}
    like = Like.objects.create(user=user, content_type=content_type, object_id=comment.id)

    # Forward the like to the inbox (if this functionality exists)
    inbox_url = f"http://backend:8000/api/authors/{userId}/inbox/"
    serializer = LikeSerializer(data=data)

    if serializer.is_valid():
        serializer.save(user=user)
        like_id = serializer.data['id'].strip('/').split('/')[-1]
        like = Like.objects.get(id=like_id)
    factory = RequestFactory()
    request = factory.post(inbox_url, data=LikeSerializer(like).data)
    IncomingPostToInbox(request, userId)
    # requests.post(inbox_url, data=LikeSerializer(like).data)

    return Response(LikeSerializer(like).data, status=status.HTTP_200_OK)

class CommentLikesList(generics.ListCreateAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        # Fetch likes for the specific comment based on the comment ID (ck)
        comment_id = self.kwargs['ck']
        return Like.objects.filter(object_id=comment_id)
    
class PublicFeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [ConditionalMultiAuthPermission]

    def get_queryset(self):
        """
        Fetches the public feed, ensuring the user sees:
        - Their own posts (excluding deleted ones).
        - Public posts from any author.
        """
        
        user = self.request.user
        
        if not user.is_authenticated:
            # Return only public posts if the user is not authenticated
            return Post.objects.filter(visibility=Post.PUBLIC).exclude(visibility=Post.DELETED).order_by("-updated_at")

        return Post.objects.filter(
            Q(author=user) |  # Show ALL posts by the user
            Q(visibility=Post.PUBLIC) # Show all public posts from all authors
        ).exclude(
            visibility=Post.DELETED # excluding deleted
        ).order_by("-updated_at")  # Show latest posts first

class FriendsFeedView(ListAPIView):

    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Fetches the Friends feed, ensuring the user sees:
        - Public posts from friends.
        - Friends-only posts if the author is a friend.
        - Unlisted posts if the author is a friend.
        """

        user = self.request.user

        # Extract only the IDs of friends
        friend_ids = user.friends.values_list('id', flat=True)  # Extract only the 'id' field

        return Post.objects.filter(
            Q(visibility=Post.FRIENDS_ONLY, author__in=friend_ids) | # Friends-only posts
            Q(visibility=Post.UNLISTED, author__in=friend_ids) # Unlisted for friends
        ).exclude(
            visibility=Post.DELETED
        ).order_by("-updated_at")  # Show latest posts first

class FollowersFeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Fetches the Followers feed, ensuring the user sees:
        - Public posts from authors followed.
        - Unlisted posts if the author is a follower.
        """

        user = self.request.user

        # Extract only the IDs of followers
        following_ids = user.following.values_list('id', flat=True) # Changed follower to following

        return Post.objects.filter(
            Q(visibility=Post.UNLISTED, author__in=following_ids)  # Unlisted for followers
        ).exclude(
            visibility=Post.DELETED
        ).order_by("-updated_at")  # Show latest posts first


class SearchUsersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get("q", "")
        local_users = []
        remote_authors = []

        # Fetch the current user's UUID from the request (if authenticated)
        current_user = request.user if request.user.is_authenticated else None
        current_user_uuid = str(current_user.id) if current_user else None

        # Fetch local users
        if query:
            local_users = User.objects.filter(Q(username__icontains=query), remote_fqid__isnull=True)
        else:
            local_users = User.objects.all()

        # Serialize local users
        local_user_list = UserSerializer(local_users, many=True).data

        # Fetch authors from all remote nodes
        remote_nodes = RemoteNode.objects.filter(is_active=True, is_my_node=False)
        for node in remote_nodes:
            try:
                url = f"{node.url.rstrip('/')}/api/authors/"
                response = requests.get(url, auth=HTTPBasicAuth(node.username, node.password))
                response.raise_for_status()  # Raise an error for bad status codes
                authors = response.json()  # Get the response JSON

                # Check if the response is a dictionary with an "items" key
                if isinstance(authors, dict) and "items" in authors:
                    authors = authors["items"]

                # Handle cases where the response is a list
                if isinstance(authors, list):
                    for author in authors:
                        # Extract the UUID from the author's ID
                        author_uuid = author.get("id", "").rstrip('/').split('/')[-1]

                        # Exclude the current user from the remote authors
                        if current_user_uuid and author_uuid == current_user_uuid:
                            continue

                        if query.lower() in author.get("username", "").lower():  # Filter by query
                            remote_authors.append(author)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching authors from {node.url}: {e}")

        # Combine local users and remote authors
        combined_results = local_user_list + remote_authors

        return Response({"users": combined_results})

@permission_classes([AllowAny])        
class ForwardGetView(APIView):
    def get(self, request, encoded_url):
        return forward_get_request(request, encoded_url)

def extract_ipv6_address(fqid):
    """
    Extracts the base URL with the IPv6 address (enclosed in square brackets) from a Fully Qualified ID (FQID).
    
    Args:
        fqid (str): The Fully Qualified ID (FQID) to parse.
    
    Returns:
        str: The base URL containing the IPv6 address.
    """
    parsed_url = urlparse(fqid)
    ipv6_address = parsed_url.netloc  # Extract the network location (host)
    if ipv6_address.startswith('[') and ipv6_address.endswith(']'):
        # If the address is already enclosed in brackets, return it
        print(f"{parsed_url.scheme}://{ipv6_address}")
        return f"{parsed_url.scheme}://{ipv6_address}"
    else:
        # Handle cases where the IPv6 address is not enclosed in brackets
        print(f"{parsed_url.scheme}://{ipv6_address}")
        return f"{parsed_url.scheme}://[{ipv6_address}]"