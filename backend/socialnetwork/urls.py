from django.contrib import admin
from django.urls import include, path
from socialnetwork.views import createUser
from .views import *
from django.conf import settings
from django.conf.urls.static import static


from socialnetwork.views import createUser, loginUser
# this urlpatterns is different from the polls urlpatterns because lab3 is a project rather than an app. 
# This urls.py is the base and forwards requests to the urls.py of the applications
urlpatterns = [
    path("core/", include("core.urls")),  # All requests sent to polls/ should be handled by polls/urls.py
    path("admin/", admin.site.urls),    # Django has a built in admin panel we will use later
    path('api/signup/', createUser, name='createUser'),
    path('api/login/', loginUser, name='user-login'),
    path('api/authors/', UsersList.as_view(), name='authors'),
    path("api/posts/", PostListCreateView.as_view(), name="post-list"),
    path("api/posts/<uuid:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("api/posts/<uuid:pk>/comment/", CreateComment, name='comment'),
    path("api/posts/<uuid:pk>/comments/", CommentsList.as_view(), name="comment-list"),
]