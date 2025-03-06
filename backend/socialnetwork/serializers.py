from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from .models import *
import markdown

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User        
        fields = ['id', 'username', 'password', 'email', 'profile_picture', 'followers', 'following', 'friends']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
            'followers': {'required': False},  # Make followers optional
            'friends': {'required': False},    # Make friends optional
        }

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

# Serializer for the Comment model
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ["id", "author", "content", "post", "created_at", "like_count"]

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
    image = serializers.ImageField(required=False)  # Allow image uploads
    author = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "image", "formatted_content", "created_at", "visibility", "like_count"]

    def get_formatted_content(self, obj):
        # Convert the content to formatted markdown
        return markdown.markdown(obj.content)

class FollowRequestSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    object = UserSerializer(read_only=True)
    class Meta:
        model = FollowRequest
        fields = ['summary', 'actor', 'object']

    def validate(self, data):
        return data
    
    def create(self, validated_data):
        summary = validated_data.get('summary')
        actor = validated_data.get('actor')
        object = validated_data.get('object')

        follow_request = FollowRequest.objects.create(summary=summary, actor=actor, object=object)
        return follow_request

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
    
    def validate(self, data):
        return data
    
    def create(self, validated_data):
        user = validated_data.get('user')
        post = validated_data.get('post')

        like = Like.objects.create(user=user, post=post)
        return like 

class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment', 'created_at']
    
    def validate(self, data):
        return data
    
    def create(self, validated_data):
        user = validated_data.get('user')
        comment = validated_data.get('comment')

        like = CommentLike.objects.create(user=user, comment=comment)
        return like 