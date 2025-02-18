from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'followers', 'friends']
        extra_kwargs = {
            # 'password': {'write_only': True},  # hides password in responses, turn this off for debugging
            'followers': {'required': False}, 
            'friends': {'required': False},  
        }

    def create(self, validated_data):
        # Extract fields and make sure they are empty by default
        followers_data = validated_data.pop('followers', [])
        friends_data = validated_data.pop('friends', [])

        # Create user without setting ManyToMany fields
        user = super().create(validated_data)
        
        # Ensure followers and friends are empty by default
        user.followers.set(followers_data)
        user.friends.set(friends_data)
        user.save()
        return user
