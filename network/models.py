from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators


class User(AbstractUser):
    following = models.ManyToManyField("self", related_name="user_follows", symmetrical=False, blank=True)
    followers = models.ManyToManyField("self", related_name="following_user", symmetrical=False, blank=True)
    profile_picture = models.URLField(max_length=240, default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png", null=True)

    def serialize(self):
        return {
        "username": self.username,
        "email": self.email
            }



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=True)
    post_body = models.CharField(max_length=240)
    date_created = models.DateTimeField(default=timezone.now)
    post_reactions = models.ManyToManyField(User, blank=True, related_name="liked")
    
    def serialize(self):
        return {
                "id": self.id,
                "user": self.user.serialize(),
                "post_body": self.post_body,
                "date_created": self.date_created,
                "post_reactions": [user.id for user in self.post_reactions.all()],
                }
    
    def __str__(self):
        return (f"New Post: {self.post_body[:15]}")
