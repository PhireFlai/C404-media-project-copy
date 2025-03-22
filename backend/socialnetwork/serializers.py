from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from .models import *
import markdown
from .utils import get_local_ip
my_ip = get_local_ip()


# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()  # Add this field
    friends = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User        
        fields = ['id', 'username', 'password', 'email', 'profile_picture', 'followers', 'following', 'friends']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
            'followers': {'required': False},  # Make followers optional
            'friends': {'required': False},    # Make friends optional
        }
        
        
    def get_id(self, obj) -> str:
        return f"http://{my_ip}:8000/api/authors/{obj.id}/"
    
    def get_friends(self, obj):
        return [f"http://{my_ip}/api/authors/{friend.id}/" for friend in obj.friends.all()]
   
    def get_followers(self, obj):
        return [f"http://{my_ip}/api/authors/{follower.id}/" for follower in obj.followers.all()]
    
    def get_following(self, obj):
        return [f"http://{my_ip}/api/authors/{following.id}/" for following in obj.following.all()]
    
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
            password=hashed_password  # Use the hashed password
        )

        # Set many-to-many relationships
        user.followers.set(followers_data)
        user.friends.set(friends_data)


        return user
# path("api/authors/<uuid:userId>/posts/<uuid:pk>/comments/<uuid:commentId>/"
# Serializer for the Comment model
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    id = serializers.SerializerMethodField()  # Add this field
    class Meta:
        model = Comment
        fields = ["id", "author", "content", "post", "created_at", "like_count", "type"]
        
    def get_id(self, obj) -> str:
        return f"http://{my_ip}:8000/api/authors/{obj.post.author.id}/posts/{obj.post.id}/comments/{obj.id}/"
    
    def validate(self, data):
        content = data.get('content')

        if not content or len(content) < 1:
            raise serializers.ValidationError("Invalid comment.")
        
        return data
    
    def create(self, validated_data):
        author = validated_data.get('author')
        content = validated_data.get('content')
        post = validated_data.get('post')

        comment = Comment.objects.create(author=author, content=content, post=post)
        return comment 

# Serializer for the Post model
class PostSerializer(serializers.ModelSerializer):
    formatted_content = serializers.SerializerMethodField()  # Add formatted content
    id = serializers.SerializerMethodField()  # Add this field
    image = serializers.ImageField(required=False)  # Allow image uploads
    author = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "image", "formatted_content", "created_at", "updated_at", "visibility", "like_count", "type"]
        
    def get_id(self, obj) -> str:
        return f"http://{my_ip}:8000/api/authors/{obj.author.id}/posts/{obj.id}/"
    
    def get_formatted_content(self, obj):
        # Convert the content to formatted markdown
        return markdown.markdown(obj.content)

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
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at', 'type']
        
            
    def get_id(self, obj) -> str:
        return f"http://{my_ip}:8000/api/liked/{obj.id}/"
    
    def validate(self, data):
        return data
    
    def create(self, validated_data):
        user = validated_data.get('user')
        post = validated_data.get('post')

        like = Like.objects.create(user=user, post=post)
        return like 

class CommentLikeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()  # Add this field
    user = UserSerializer(read_only=True)
    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment', 'created_at', 'type']
        
    def get_id(self, obj) -> str:
        return f"http://{my_ip}:8000/api/liked/{obj.id}/"
    
    def validate(self, data):
        return data
    
    def create(self, validated_data):
        user = validated_data.get('user')
        comment = validated_data.get('comment')

        like = CommentLike.objects.create(user=user, comment=comment)
        return like 