from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("following/<int:user_id>", views.following, name="following"),
    path("user/<int:user_id>", views.user, name="user"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
     
    # API Routes
    path("like/<int:post_id>", views.like, name="like"),
    path("unlike/<int:post_id>", views.unlike, name="unlike"),
    path("edit/<int:post_id>", views.edit, name="edit"),

    path("follow_user/<int:user_id>", views.follow_user, name="follow_user"),
    path("unfollow_user/<int:user_id>", views.unfollow_user, name="unfollow_user"),
]
