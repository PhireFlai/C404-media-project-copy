from django.contrib import admin
from django.urls import include, path

# this urlpatterns is different from the polls urlpatterns because lab3 is a project rather than an app. 
# This urls.py is the base and forwards requests to the urls.py of the applications
urlpatterns = [
    path("core/", include("core.urls")),  # All requests sent to polls/ should be handled by polls/urls.py
    path("admin/", admin.site.urls),    # Django has a built in admin panel we will use later
]