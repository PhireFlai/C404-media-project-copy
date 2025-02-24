from django.test import TestCase
from django.apps import apps
from django.db import models
from django.conf import settings

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Post, Comment
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from ..views import *

User = get_user_model()

from django.contrib.postgres.fields import ArrayField

class NoArrayFieldsTestCase(TestCase):
    """Test to ensure no array fields are stored in the database. NM12"""

    def test_no_array_fields(self):
        app_models = apps.get_app_config('socialnetwork').get_models()
        for model in app_models:
            for field in model._meta.get_fields():
                if ArrayField:
                    self.assertNotIsInstance(field, ArrayField, f"{model.__name__} has an ArrayField: {field.name}")

class RelationalDatabaseTestCase(TestCase):
    """Test to ensure the application uses a relational database. NM11"""

    def test_database_configuration(self):
        db_engine = settings.DATABASES['default']['ENGINE']
        self.assertIn('django.db.backends.', db_engine, "The database engine is not a relational database.")
        self.assertNotIn('sqlite3', db_engine, "SQLite should only be used for local testing.")

class RESTfulInterfaceTestCase(APITestCase):
    """Test to ensure the application provides a RESTful interface. NM5"""
    # Not sure if we need to separately test this, since the application is built using Django REST
    # framework and we are testing the API endpoints in other test cases

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.token = Token.objects.create(user=cls.user)
        cls.post = Post.objects.create(title="Test Post", content="Content here", author=cls.user)
        cls.comment = Comment.objects.create(content="Test Comment", author=cls.user, post=cls.post)

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_posts(self):
        """Test retrieving posts."""
        response = self.client.get(reverse('post-list', kwargs={'userId': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_and_retrieve_posts_with_different_visibilities(self):
        """Test if all the posts including the deleted ones are stored and accessible from the database. NM-14"""
        # Create posts with different visibilities
        deleted_post = Post.objects.create(
            title="Deleted Post",
            content="This post is marked as deleted",
            author=self.user,
            visibility=Post.DELETED
        )
        public_post = Post.objects.create(
            title="Public Post",
            content="This is a public post",
            author=self.user,
            visibility=Post.PUBLIC
        )
        unlisted_post = Post.objects.create(
            title="Unlisted Post",
            content="This is an unlisted post",
            author=self.user,
            visibility=Post.UNLISTED
        )
        friends_only_post = Post.objects.create(
            title="Friends Only Post",
            content="This is a friends-only post",
            author=self.user,
            visibility=Post.FRIENDS_ONLY
        )

        # Fetch all posts directly from the database
        posts = Post.objects.filter(author=self.user)
        post_ids = [str(post.id) for post in posts]

        # Check that all created posts are in the response
        self.assertIn(str(deleted_post.id), post_ids)
        self.assertIn(str(public_post.id), post_ids)
        self.assertIn(str(unlisted_post.id), post_ids)
        self.assertIn(str(friends_only_post.id), post_ids)
