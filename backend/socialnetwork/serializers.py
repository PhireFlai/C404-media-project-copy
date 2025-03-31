from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from .models import *
import markdown
from django.contrib.contenttypes.models import ContentType
from .utils import get_local_ip
my_ip = get_local_ip()
print(my_ip)


# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)  # Allow the `id` field to be explicitly set
    friends = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User        
        fields = ['id', 'username', 'password', 'profile_picture', 'followers', 'following', 'friends', 'remote_fqid', 'displayName', 'github', 'is_approved', 'host', 'page', 'profileImage', 'type', 'github_etag', 'friends', 'followers']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
            'followers': {'required': False},  # Make followers optional
            'friends': {'required': False},    # Make friends optional
            'is_approved': {'write_only': True},  # Ensure is_approved is write-only
        }
        
        
    def get_id(self, obj) -> str:
        return f"http://[{my_ip}]/api/authors/{obj.id}/"
    
    def get_friends(self, obj):
        return [f"http://[{my_ip}]/api/authors/{friend.id}/" for friend in obj.friends.all()]
   
    def get_followers(self, obj):
        return [f"http://[{my_ip}]/api/authors/{follower.id}/" for follower in obj.followers.all()]
    
    def get_following(self, obj):
        return [f"http://[{my_ip}]/api/authors/{following.id}/" for following in obj.following.all()]
    
    def validate_password(self, value):
        # Validate the password using Django's password validation
        validate_password(value)
        return value

    def create(self, validated_data):
        # Extract and remove many-to-many fields
        followers_data = validated_data.pop('followers', [])
        friends_data = validated_data.pop('friends', [])

        # Hash the password
        password = validated_data.pop('password')
        hashed_password = make_password(password)

        # Create the user instance
        user = User.objects.create(
            **validated_data,
            password=hashed_password,  # Use the hashed password
        )

        # Set many-to-many relationships
        user.followers.set(followers_data)
        user.friends.set(friends_data)

        # Assign values to non-many-to-many fields
        user.displayName = validated_data.get('username', '')

        current_remote_node = None
        try:
            current_remote_node = RemoteNode.objects.get(is_my_node=True)
        except Exception as e:
            print(f"Error fetching remote node: {e}")

        # Convert user.id to a string before checking or splitting
        user_id_str = str(user.id)
        if 'authors' in user_id_str:
            # Extract the host from the user ID
            host_base = user_id_str.split('authors')[0]
            user.host = host_base
        
        # If the user id does not have http, append our remote node url
        if 'http' not in user_id_str:
            user.host = current_remote_node.url + 'api/'

        if not user.page:
            page_path = current_remote_node.url + user_id_str
            user.page = page_path

        user.profileImage = user.profile_picture.url if user.profile_picture else None

        user.save()

        return user

# path("api/authors/<uuid:userId>/posts/<uuid:pk>/comments/<uuid:commentId>/"
# Serializer for the Comment model
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    id = serializers.SerializerMethodField()  # Add this field
    post = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ["id", "author", "comment", "post", "created_at", "like_count", "type", "contentType", "published"]
    
    def get_post(self, obj) -> str:
            return f"http://[{my_ip}]:8000/api/authors/{obj.post.author.id}/posts/{obj.post.id}/"

    def get_id(self, obj) -> str:
        return f"http://[{my_ip}]:8000/api/authors/{obj.post.author.id}/posts/{obj.post.id}/comments/{obj.id}/"
    
    def validate(self, data):
        comment = data.get('comment')

        if not comment or len(comment) < 1:
            raise serializers.ValidationError("Invalid comment.")
        
        return data
    
    def create(self, validated_data):
        author = validated_data.get('author')
        comment = validated_data.get('comment')
        post = validated_data.get('post')

        comment = Comment.objects.create(author=author, comment=comment, post=post)
        return comment 

# Serializer for the Post model
class PostSerializer(serializers.ModelSerializer):
    formatted_content = serializers.SerializerMethodField()  # Add formatted content
    id = serializers.SerializerMethodField()  # Add this field
    image = serializers.ImageField(required=False, use_url=False)  # Allow image uploads
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "image", "formatted_content", "created_at", "published", "visibility", "like_count", "type", "remote_fqid", "comments", "description", "page", "contentType"]

    
    def get_id(self, obj) -> str:
        return f"http://[{my_ip}]:8000/api/authors/{obj.author.id}/posts/{obj.id}/"
    
    def get_formatted_content(self, obj):
        # Convert the content to formatted markdown
        return markdown.markdown(obj.content)

    def create(self, validated_data):
        post = Post.objects.create(
            **validated_data
        )

        post.description = post.title
        # author page is post page
        post.page = post.author.page if post.author.page else None

        post.save()

        return post

class FollowRequestSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    object = UserSerializer(read_only=True)
    class Meta:
        model = FollowRequest
        fields = ['summary', 'actor', 'object', 'type']

    def validate(self, data):
        return data
    
    def create(self, validated_data):
        summary = validated_data.get('summary')
        actor = validated_data.get('actor')
        object = validated_data.get('object')

        follow_request = FollowRequest.objects.create(summary=summary, actor=actor, object=object)
        return follow_request
#   path("api/authors/<uuid:userId>/posts/<uuid:pk>/like/", AddLike, name='add-like'),
#   path("api/authors/<uuid:userId>/posts/<uuid:pk>/likes/", LikesList.as_view(), name="likes-list"),
#   path("api/authors/<uuid:userId>/posts/<uuid:pk>/comments/<uuid:ck>/like/", AddCommentLike, name='add-like'),
#   path("api/authors/<uuid:userId>/posts/<uuid:pk>/comments/<uuid:ck>/likes/", CommentLikesList.as_view(), name="likes-list"),
#   api/liked/<uuid:id>/
class LikeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()  # Add this field
    user = UserSerializer(read_only=True)
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field='model'  # This will display the model name (e.g., 'post' or 'comment')
    )

    class Meta:
        model = Like
        fields = ['id', 'user', 'content_type', 'object_id', 'created_at', 'type',]        
            
    def get_id(self, obj) -> str:
        return f"http://[{my_ip}]:8000/api/liked/{obj.id}/"

    def validate(self, data):
        # Ensure the object_id corresponds to the content_type
        content_type = data.get('content_type')
        object_id = data.get('object_id')

        model = content_type.model_class()
        if not model.objects.filter(id=object_id).exists():
            raise serializers.ValidationError(f"The object with ID {object_id} does not exist in {content_type}.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user  # Get the user from the request context
        content_type = validated_data.get('content_type')
        object_id = validated_data.get('object_id')

        like = Like.objects.create(user=user, content_type=content_type, object_id=object_id)
        return like
