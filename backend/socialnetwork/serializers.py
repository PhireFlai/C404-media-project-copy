from rest_framework import serializers
from .models import User, Post
import markdown

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'followers', 'friends']
        
    def create(self, validated_data):
        validated_data['followers'] = []  # Ensure no followers are set by default
        validated_data['friends'] = []  # Ensure no friends are set by default
        return super().create(validated_data)
    
class PostSerializer(serializers.ModelSerializer):
    formatted_content = serializers.SerializerMethodField()  # Add formatted content

    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "formatted_content", "created_at"]

    def get_formatted_content(self, obj):
        return markdown.markdown(obj.content)