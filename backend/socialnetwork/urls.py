from django.contrib import admin
from django.urls import include, path
from socialnetwork.views import createUser, loginUser
from .views import *
from django.conf import settings
from django.conf.urls.static import static

# This urls.py is the base and forwards requests to the urls.py of the applications
urlpatterns = [
    path("core/", include("core.urls")),  # Includes URLs from the core application
    path("admin/", admin.site.urls),  # Admin site URLs
    path('api/signup/', createUser, name='createUser'),  # Endpoint for user signup
    path('api/login/', loginUser, name='user-login'),  # Endpoint for user login
    path('api/authors/', UsersList.as_view(), name='authors'),  # Endpoint to list and create users
    path("api/authors/<uuid:userId>/posts/", PostListCreateView.as_view(), name="post-list"),  # Endpoint to list and create posts for a specific user
    path('api/authors/<uuid:userId>/', UserProfileView.as_view(), name='user-profile'),  # Endpoint to retrieve and update a user's profile
    path('api/authors/<uuid:userId>/update-picture/', updateUserProfile, name='update-user-profile'),  # Endpoint to update a user's profile picture
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/", PostDetailView.as_view(), name="post-detail"),  # Endpoint to retrieve, update, and delete a specific post
    path("api/authors/<uuid:author>/inbox/", PostComment, name='post-comment'),  # Endpoint to post a comment to an author's inbox
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/comment/", CreateComment, name='comment'),  # Endpoint to create a comment on a post
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/comments/", CommentsList.as_view(), name="comment-list"),  # Endpoint to list and create comments for a specific post
    path("api/public-posts/", PublicPostsView.as_view(), name="public-posts"),  # Endpoint to list public posts
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)