from django.contrib import admin
from django.urls import include, path, re_path
from socialnetwork.views import createUser
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from socialnetwork.views import createUser, loginUser

schema_view = get_schema_view(
    openapi.Info(
        title="Team Cyan API",
        default_version="v1",
        description="API documentation for Project Part 1",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# This urls.py is the base and forwards requests to the urls.py of the applications
urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),  # Swagger UI for API documentation
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),  # ReDoc for API documentation
    path("core/", include("core.urls")),  # Includes URLs from the core application
    path("admin/", admin.site.urls),  # Admin site URLs
    path('api/signup/', createUser, name='createUser'),  # Endpoint for user signup
    path('api/login/', loginUser, name='user-login'),  # Endpoint for user login
    path('api/authors/', UsersList.as_view(), name='authors'),  # Endpoint to list and create users
    path("api/authors/<uuid:userId>/posts/", PostListCreateView.as_view(), name="post-list"),  # Endpoint to list and create posts for a specific user
    path('api/authors/<uuid:userId>/', UserProfileView.as_view(), name='user-profile'),  # Endpoint to retrieve and update a user's profile
    path('api/authors/<uuid:userId>/update-picture/', updateUserProfile, name='update-user-profile'),  # Endpoint to update a user's profile picture
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/", PostDetailView.as_view(), name="post-detail"),  # Endpoint to retrieve, update, and delete a specific post
    path("api/authors/<uuid:receiver>/inbox/", PostToInbox, name='post-to-inbox'),  # Endpoint to post to author's inbox
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/comment/", CreateComment, name='comment'),  # Endpoint to create a comment on a post
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/comments/", CommentsList.as_view(), name="comment-list"),  # Endpoint to list and create comments for a specific post
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/comments/<uuid:commentId>/", GetComment.as_view(), name="get-comment"),  # Endpoint to get a specific comment on a specific post
    path("api/authors/<uuid:userId>/commented/", GetCommented.as_view(), name='commented'),  # Endpoint to get all comments made by a specific author
    path("api/authors/<uuid:userId>/commented/<uuid:commentId>/", GetCommentFromCommented.as_view(), name='get-commented-comment'),  # Endpoint to get a specific comment made by a specific author
    path("api/public-posts/", PublicPostsView.as_view(), name="public-posts"),  # Endpoint to list public posts
    path("api/authors/<uuid:userId>/friends-posts/", FriendsPostsView.as_view(), name="friends-posts"),
    path("api/authors/<uuid:userId>/followers/", FollowersList.as_view(), name="user-followers"), # Endpoint to list followers of a specific user
    path("api/authors/<uuid:userId>/following/", FollowingList.as_view(), name="user-follows"), # Endpoint to list users that a specific user follows
    path("api/authors/<uuid:objectId>/follow-requests/", FollowRequestListView.as_view(), name='follow-request-list'),
    path("api/authors/<uuid:actorId>/follow/authors/<uuid:objectId>/", CreateFollowRequest, name='create-follow-request'),
    path("api/authors/<uuid:objectId>/accept-follow-request/authors/<uuid:actorId>/", AcceptFollowRequest, name='accept-follow-request'),
    path("api/authors/<uuid:followerId>/unfollow/authors/<uuid:followedId>/", Unfollow, name='unfollow'),
    path("api/authors/<uuid:followedId>/remove-follower/authors/<uuid:followerId>/", RemoveFollower, name='remove-follower'),
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/like/", AddLike, name='add-like'),
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/likes/", LikesList.as_view(), name="likes-list"),
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/comments/<uuid:ck>/like/", AddCommentLike, name='add-like'),
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/comments/<uuid:ck>/likes/", CommentLikesList.as_view(), name="likes-list"),
    path("api/posts/<uuid:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("api/authors/feed/", UserFeedView.as_view(), name="user-feed"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)