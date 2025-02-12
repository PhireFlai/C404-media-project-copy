from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'followers', 'friends']
        
    def create(self, validated_data):
        validated_data['followers'] = []  # Ensure no followers are set by default
        validated_data['friends'] = []  # Ensure no friends are set by default
        return super().create(validated_data)