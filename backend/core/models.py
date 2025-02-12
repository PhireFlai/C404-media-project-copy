import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='following', blank=True
    )
    
    
    
    # revist adding profile pictures later
    # profile_picture = models.ImageField()
