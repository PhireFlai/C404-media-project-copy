from django.urls import path
from . import views
from .views import createUser

# urlpatterns contains all of the routes that this application supports routing for.
# this routes traffic from polls/ to the index function that we defined earlier in the views file.
urlpatterns = [
    path("test", views.test, name="test"),
    path('api/signup/', views.createUser, name='createUser')
]