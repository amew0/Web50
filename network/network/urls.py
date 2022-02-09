
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:userId>", views.profile, name="profile"),
    path("<int:userId>/following", views.following, name="following"),

    #API route
    path("posts/<int:post_id>", views.posts, name="posts"),
    path("posts", views.allPosts, name="allPosts"),
    path("user/<int:userId>", views.user, name="user")
]
