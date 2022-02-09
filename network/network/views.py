from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse    
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from .models import *
from django.forms import ModelForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

class NewPost(ModelForm):
    class Meta:
        model = Post
        fields = ['content']

def index(request):
    if request.method == "POST":
        Content = request.POST["content"]
        UserP = User.objects.get(pk = request.user.id)
        Likes = 0
        DateNtime = datetime.now()

        create = Post(
                content = Content,
                userP = UserP,
                likes = Likes,
                dateNtime = DateNtime)
        create.save()

    posts = Post.objects.all().order_by('-dateNtime')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
            "posts": posts,
            "NewPost": NewPost(),
            "check": User.objects.all(),
            "page_obj": page_obj
            })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
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
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        except ValueError:
            return render(request, "network/register.html", {
                "message": "Check if some fields are empty."
                })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, userId):
    if(request.user.id == None):
        return render(request, "network/error.html")
    else:
        numOfFollowers = len(User.objects.get(pk = userId).follower.all())
        numOfFollowing = len(User.objects.get(pk=userId).following.all())
        posts = User.objects.get(id = userId).userspost.all().order_by('-dateNtime')

        authenticated = True if userId == request.user.id else False

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/profile.html", {
            "numOfFollowers" : numOfFollowers,
            "numOfFollowing" : numOfFollowing,
            "posts" : posts,
            "authenticated" : authenticated,
            "userId": userId,
            "currentUser" : User.objects.get(pk=request.user.id),
            "page_obj": page_obj
            })

@csrf_exempt
def posts(request,post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "GET":
        return JsonResponse(post.serialize(), safe=False)
    # Update number of likes of the post 
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
            print(post.content)
            post.dateNtime = datetime.now()
        if data.get("likes") is not None:
            post.likes = data["likes"]
        post.save()
        return HttpResponse(status=204)

def allPosts(request):
    allposts = Post.objects.all().order_by("-dateNtime")
    if request.method == "GET":
        return JsonResponse([post.serialize() for post in allposts] ,safe=False)

def following(request, userId):
    numOfFollowing = len(User.objects.get(id=userId).following.all())
    posts = []
    temp = []
    for i in range(numOfFollowing):
        aPost = User.objects.get(id=userId).following.all()[i].userspost.all().order_by("-dateNtime")
        posts.append(aPost)
    if (len(posts) == 0):
        posts = "noPosts"

    else:
        for i in posts:
            for j in i:
                temp.append(j)
        posts = temp

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "query": posts,
        "page_obj": page_obj
        })

@csrf_exempt
def user(request, userId):
    Auser = User.objects.get(pk=userId)
    if request.method == "GET":
        return JsonResponse(Auser.serialize(), safe=False)
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("follower") is not None:
           print(len(data["follower"]))
           Auser.follower.set([User.objects.get(username=data["follower"][x]) for x in range(0,len(data["follower"]))])
        Auser.save()
        return HttpResponse(status=204)