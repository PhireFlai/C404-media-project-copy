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

# this urlpatterns is different from the polls urlpatterns because lab3 is a project rather than an app. 
# This urls.py is the base and forwards requests to the urls.py of the applications
urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("core/", include("core.urls")),
    path("admin/", admin.site.urls),
    path('api/signup/', createUser, name='createUser'),
    path('api/login/', loginUser, name='user-login'),
    path('api/authors/', UsersList.as_view(), name='authors'),
    path("api/authors/<uuid:userId>/posts/", PostListCreateView.as_view(), name="post-list"),
    path('api/authors/<uuid:userId>/', UserProfileView.as_view(), name='user-profile'),
    path('api/authors/<uuid:userId>/update-picture/', updateUserProfile, name='update-user-profile'),  
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("api/authors/<uuid:author>/inbox/", PostComment, name='post-comment'),
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/comment/", CreateComment, name='comment'),
    path("api/authors/<uuid:userId>/posts/<uuid:pk>/comments/", CommentsList.as_view(), name="comment-list"),
    path("api/public-posts/", PublicPostsView.as_view(), name="public-posts"),  # New path for public posts
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)