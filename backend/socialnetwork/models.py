import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os

def user_profile_picture_path(instance, filename):
    # Extract the file extension from the original filename
    extension = os.path.splitext(filename)[1]
    # Return the new file path with the user's ID and the original file extension
    return f'profile_pictures/{instance.id}{extension}'

class User(AbstractUser):
    # username = models.CharField(max_length=32, unique=True)
    # password = models.CharField(max_length=128)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True)
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='following', blank=True
    )
    friends = models.ManyToManyField(
        'self', symmetrical=True, blank=True
    )
    
    # Fix conflict with Django’s auth system
    groups = models.ManyToManyField("auth.Group", related_name="socialnetwork_users", blank=True)
    user_permissions = models.ManyToManyField("auth.Permission", related_name="socialnetwork_users_permissions", blank=True)
    
    def __str__(self):
        return self.username  # Display the username in the admin panel


    def save(self, *args, **kwargs):
        # Check if the profile picture is being updated
        if self.pk:
            old_user = User.objects.get(pk=self.pk)
            if old_user.profile_picture and old_user.profile_picture != self.profile_picture:
                old_user.profile_picture.delete(save=False)
        super().save(*args, **kwargs)
        
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    # Author Now optional
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Author can be null for now
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)