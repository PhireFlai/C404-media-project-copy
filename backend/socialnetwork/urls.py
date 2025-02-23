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
    path("api/posts/", PostListCreateView.as_view(), name="post-list"),
    path('api/profile/<uuid:userId>/', getUserProfile, name='get-user-profile'),  # GET profile
    path('api/profile/<uuid:userId>/update-picture/', updateUserProfile, name='update-user-profile'),  # PUT profile
    path('api/profile/<uuid:userId>/update-username/', updateUsername, name='update-username'),  # PUT username
    path("api/posts/<uuid:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("api/authors/<uuid:author>/inbox/", PostComment, name='post-comment'),
    path("api/posts/<uuid:pk>/comment/", CreateComment, name='comment'),
    path("api/posts/<uuid:pk>/comments/", CommentsList.as_view(), name="comment-list"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)