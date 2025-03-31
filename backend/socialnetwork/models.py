import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.fields import GenericForeignKey,  GenericRelation
from django.contrib.contenttypes.models import ContentType

def user_profile_picture_path(instance, filename):
    # Extract the file extension from the original filename
    extension = os.path.splitext(filename)[1]
    # Return the new file path with the user's ID and the original file extension
    return f'profile_pictures/{instance.id}{extension}'

class User(AbstractUser):
    # username = models.CharField(max_length=32, unique=True)
    # password = models.CharField(max_length=128)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.TextField(default="author", editable=False)
    #profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, default="profile_pictures/default.png", null=True, blank=True)
    
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='following', blank=True
    )
    friends = models.ManyToManyField(
        'self', symmetrical=True, blank=True
    )
    
    # Fix conflict with Django’s auth system
    groups = models.ManyToManyField("auth.Group", related_name="socialnetwork_users", blank=True)
    user_permissions = models.ManyToManyField("auth.Permission", related_name="socialnetwork_users_permissions", blank=True)
    
    is_approved = models.BooleanField(default=False)

    github = models.URLField(max_length=200, blank=True, null=True)
    github_etag = models.CharField(max_length=250, blank=True, null=True)

    remote_fqid = models.CharField(max_length=250, blank=True, null=True)

    displayName = models.CharField(max_length=100, blank=True, null=True)
    host = models.CharField(max_length=250, blank=True, null=True)
    page = models.CharField(max_length=250, blank=True, null=True)

    profileImage = models.CharField(max_length=250, blank=True, null=True)
    
    def __str__(self):
        return self.username  # Display the username in the admin panel


    def save(self, *args, **kwargs):
        if self.pk:  # Ensure self.pk is not None
            try:
                old_user = User.objects.get(pk=self.pk)
                if old_user.profile_picture and old_user.profile_picture != self.profile_picture:
                    old_user.profile_picture.delete(save=False)  # Delete old picture
            except ObjectDoesNotExist:
                pass  # User doesn't exist yet, so nothing to delete

        super().save(*args, **kwargs)  # Save the instance

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type = models.TextField(default="like", editable=False)
    
    # Fields for Generic Foreign Key
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE
    )
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")
    
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.user.username} likes {self.content_object}"
    
class Post(models.Model):
    PUBLIC = 'PUBLIC'
    FRIENDS = 'FRIENDS'
    UNLISTED = 'UNLISTED'
    DELETED = 'DELETED'

    VISIBILITY_CHOICES = [
        (PUBLIC, 'PUBLIC'),
        (FRIENDS, 'FRIENDS'),
        (UNLISTED, 'UNLISTED'),
        (DELETED, 'DELETED')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.TextField(default="post", editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default=PUBLIC)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(auto_now=True)
    remote_fqid = models.CharField(max_length=250, blank=True, null=True)
    page = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contentType = models.TextField(default="text/plain", editable=False)

    likes = GenericRelation(Like)  # Enable reverse relation

    @property
    def like_count(self):
        try:
            return self.likes.count()
        except Exception:
            return 0

    def __str__(self):
        return self.title  # Display the title in the admin panel

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.TextField(default="comment", editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Author can be null for now
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    published = models.DateTimeField(auto_now=True)
    contentType = models.CharField(default="text/markdown", max_length=50, editable=False)

    likes = GenericRelation(Like)  # Enable reverse relation

    @property
    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.author.username} comments {self.content}"

class FollowRequest(models.Model):
    type = models.TextField(default="follow", editable=False)
    summary = models.TextField()
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_follow_request")
    object = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_follow_request")


class EnvironmentSetting(models.Model):
    require_admin_approval_for_signup = models.BooleanField(default=False)

    def __str__(self):
        return f"Require admin approval for signup: {self.require_admin_approval_for_signup}"

class RemoteNode(models.Model):
    url = models.URLField(unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_my_node = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.url} ({'Active' if self.is_active else 'Disabled'})"