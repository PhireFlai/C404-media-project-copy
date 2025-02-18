from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from .models import User, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'followers', 'friends']
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
    
class PostSerializer(serializers.ModelSerializer):
    formatted_content = serializers.SerializerMethodField()  # Add formatted content

    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "formatted_content", "created_at"]

    def get_formatted_content(self, obj):
        return markdown.markdown(obj.content)