import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django import forms
from django.forms import Textarea
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_body']
        widget = {
                'post_body': Textarea(attrs={'cols': 40, 'rows': 5}),
                }


def index(request):
    posts = Post.objects.all().order_by('-date_created')
    paginated_posts = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginated_posts.get_page(page_number)

    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, 'network/index.html', {
            "page_obj": page_obj,
            "create_post": NewPostForm(),
            })


@login_required
def following(request, user_id):
    user = User.objects.get(id=request.user.id)
    following_users = user.following.all()
    posts = Post.objects.filter(user__in=following_users).all()
    posts = posts.order_by('-date_created')

    paginated_posts = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginated_posts.get_page(page_number)
    return render(request, "network/following.html", {
        "user": user,
        "following_users": following_users,
        "posts": posts,
        "page_obj": page_obj,
        })


@login_required
@csrf_exempt
def edit(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)


    if request.method == "PUT":
        if post.user.id == request.user.id:
            data = json.loads(request.body)
            if data.get("post_body") is not None:
                post.post_body = data["post_body"]
            post.save()
            return JsonResponse(post.serialize())
        else:
            return JsonResponse({"error": "You cannot edit another users post."}, status=404)



class FollowOrUnfollowUserForm(forms.Form):
    fields = ['follow', 'unfollow']



@login_required
@csrf_exempt
def follow_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = FollowOrUnfollowUserForm(request.POST)
        if form.is_valid():
            if ["follow"]:
                user.followers.add(request.user.id)
                request.user.following.add(user.id)
                return HttpResponseRedirect(reverse("user", kwargs={'user_id': user_id}))
            return HttpResponseRedirect(reverse("user", kwargs={'user_id': user_id}))
        return HttpResponseRedirect(reverse("user", kwargs={'user_id': user_id}))
    return HttpResponseRedirect(reverse("user", kwargs={'user_id': user_id}))



@login_required
@csrf_exempt
def unfollow_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = FollowOrUnfollowUserForm(request.POST)
        if form.is_valid():
            if ["unfollow"]:
                user.followers.remove(request.user.id)
                request.user.following.remove(user.id)
                return HttpResponseRedirect(reverse("user", kwargs={'user_id': user_id}))
            return HttpResponseRedirect(reverse("user", kwargs={'user_id': user_id}))
        return HttpResponseRedirect(reverse("user", kwargs={'user_id': user_id}))
    return HttpResponseRedirect(reverse("user", kwargs={'user_id': user_id}))



class LikeOrUnlikeForm(forms.Form):
    fields = ['like', 'unliked']



@csrf_exempt
@login_required
def like(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("liked") is not None:
          post.post_reactions.add(request.user)
        post.save()
        return JsonResponse(post.serialize())


@csrf_exempt
@login_required
def unlike(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("unliked") is not None:
          post.post_reactions.remove(request.user)
        post.save()
        return JsonResponse(post.serialize())


def user(request, user_id):
    user = User.objects.get(id=user_id)
    posts = user.posts.all()
    posts = posts.order_by('-date_created')
    following = user.following.all()
    followers = user.followers.all()

    paginated_posts = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginated_posts.get_page(page_number)

    return render(request, "network/user.html", {
        "user": user,
        "following": following,
        "followers": followers,
        "posts": posts,
        "follow_user": FollowOrUnfollowUserForm(),
        "page_obj": page_obj
        })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        profile_picture = request.POST["profile_picture"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            if profile_picture:
                user.profile_picture=profile_picture
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
