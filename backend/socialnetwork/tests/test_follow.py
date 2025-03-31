from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from ..models import FollowRequest, RemoteNode

User = get_user_model()

class FollowAPITestCase(APITestCase):
    """Test suite for the Follow API."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.other_user = User.objects.create_user(username='otheruser', password='password')

        cls.user.remote_fqid = f"http://testserver/api/authors/{cls.user.id}/"
        cls.user.save()

        cls.other_user.remote_fqid = f"http://testserver/api/authors/{cls.other_user.id}/"
        cls.other_user.save()

        cls.token = Token.objects.create(user=cls.user)
        cls.other_token = Token.objects.create(user=cls.other_user)

        # Create a dummy RemoteNode to satisfy the lookup
        RemoteNode.objects.create(
            url="http://testserver/",
            username="testuser",
            password="testpass",
            is_active=True,
            is_my_node=False
        )


    def setUp(self):
        """Login a user for testing."""
        self.client.login(username='testuser', password='password')
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_send_follow_request(self):
        """Test sending a follow request."""
        summary = f'{self.user.username} wants to follow {self.other_user.username}'

        actor_id = self.user.remote_fqid.rstrip("/") + "/"
        object_id = self.other_user.remote_fqid.rstrip("/") + "/"

        data = {
            "type": "follow",
            "summary": summary,
            "actor": {
                "id": actor_id,
                "username": self.user.username,
                "email": self.user.email,
                "profile_picture": self.user.profile_picture.url,
                "followers": [],
                "following": [],
                "friends": [],
                "remote_fqid": actor_id,
            },
            "object": {
                "id": object_id,
                "username": self.other_user.username,
                "email": self.other_user.email,
                "profile_picture": self.other_user.profile_picture.url,
                "followers": [],
                "following": [],
                "friends": [],
                "remote_fqid": object_id,
            }
        }

        print("Actor ID:", actor_id)
        print("Object ID:", object_id)

        response = self.client.post(
            f'/api/authors/{self.user.id}/follow/authors/{self.other_user.id}/',
            data,
            format='json'
        )

        print("Follow request response:", response.status_code, response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FollowRequest.objects.filter(actor=self.user, object=self.other_user).exists())

    def list_follow_requests(self):
        response = self.client.get(f'api/authors/{self.other_user.id}/follow-requests/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_accept_follow_request(self):
        """Test accepting a follow request."""
        FollowRequest.objects.create(actor=self.user, object=self.other_user)
        self.client.login(username='otheruser', password='password')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
        response = self.client.post(f'/api/authors/{self.other_user.id}/accept-follow-request/authors/{self.user.id}/?action=accept')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user, self.other_user.followers.all())

    def test_reject_follow_request(self):
        """Test rejecting a follow request."""
        FollowRequest.objects.create(actor=self.user, object=self.other_user)
        self.client.login(username='otheruser', password='password')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
        response = self.client.post(f'/api/authors/{self.other_user.id}/accept-follow-request/authors/{self.user.id}/?action=reject')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.user, self.other_user.followers.all())

    def test_unfollow_user(self):
        """Test unfollowing a user."""
        self.other_user.followers.add(self.user)
        response = self.client.post(f'/api/authors/{self.user.id}/unfollow/authors/{self.other_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.user, self.other_user.followers.all())
        self.assertNotIn(self.user, self.other_user.friends.all())
        self.assertNotIn(self.other_user, self.user.friends.all())

    def test_remove_follower(self):
        """Test removing a follower."""
        self.user.followers.add(self.other_user)
        response = self.client.post(f'/api/authors/{self.user.id}/remove-follower/authors/{self.other_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.other_user, self.user.followers.all())
        self.assertNotIn(self.other_user, self.user.friends.all())
        self.assertNotIn(self.user, self.other_user.friends.all())
