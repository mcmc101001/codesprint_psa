import re
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Value
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import CustomUser, Request, Task, Reward, User, Follow, Cart

from datetime import datetime

# Main page
@login_required(login_url='/main/login')
def index(request):
    current_user = CustomUser.objects.get(user=request.user)
    following = Follow.objects.filter(follower = current_user)
    requests = Request.objects.filter(requested = current_user)
    return render(request, "main/index.html", {
        "following": following,
        "requests": requests,
    })

#### SOCIAL MODULE ####
# Users search page
@login_required(login_url='/main/login')
def users(request):
    current_user = CustomUser.objects.get(user=request.user)
    other_users = CustomUser.objects.all().exclude(pk=current_user.pk)
    requested = []
    following = []
    for user in other_users:
        if Follow.objects.filter(follower = current_user, following = user):
            following.append(user)
        elif Request.objects.filter(requestor=current_user, requested=user):
            requested.append(user)
    return render(request, 'main/users.html', {
        "user_list": other_users,
        "following": following,
        "requested": requested,
    })

def follow(request):
    if request.method == "POST":
        current_user = CustomUser.objects.get(user=request.user)
        requested = CustomUser.objects.get(pk = int(request.POST['user_id']))
        request = Request(requestor=current_user, requested=requested)
        request.save()
        return HttpResponseRedirect(reverse('main:users'))

def modify_request(request):
    if request.method == "POST":
        current_user = CustomUser.objects.get(user=request.user)
        try:
            outcome = request.POST["outcome"]
        except:
            outcome = "NO"
        requestor_id = int(request.POST["requestor_id"])
        requestor = CustomUser.objects.get(pk = requestor_id)
        if outcome == "True":
            follow = Follow(follower=requestor, following=current_user, date=datetime.now().date())
            follow.save()
        request = Request.objects.get(requestor=requestor, requested=current_user)
        request.delete()
        return HttpResponseRedirect(reverse('main:index'))

@login_required(login_url='/main/login')
def user_profile(request, user_id):
    user = CustomUser.objects.get(pk = user_id)
    tasks = user.tasks.all()
    return render(request, 'main/user_profile.html', {
        "user": user,
        "tasks": tasks,
    })

#### PROFILE MODULE ####
# Profile page
@login_required(login_url='/main/login')
def profile(request):
    current_user = CustomUser.objects.get(user=request.user)
    tasks = current_user.tasks.all()
    return render(request, 'main/profile.html', {
        "user": current_user,
        "tasks": tasks,
    })

@login_required(login_url='/main/login')
def edit_profile(request):
    current_user = CustomUser.objects.get(user=request.user)
    return render(request, 'main/edit_profile.html', {
        "user": current_user,
    })

@login_required(login_url='/main/login')
def update_profile(request):
    if request.method == "POST":
        is_duplicate = False
        current_user = CustomUser.objects.get(user=request.user)
        username = request.POST["username"]
        if User.objects.filter(username = username).exclude(pk=current_user.user.pk):
            is_duplicate = True
        else:
            current_user.user.username = username
        email = request.POST["email"]
        if CustomUser.objects.filter(email = email).exclude(pk=current_user.pk):
            is_duplicate = True
        else:
            current_user.email = email
        department = request.POST["department"]
        current_user.department = department
        current_user.user.save()
        current_user.save()
        tasks = current_user.tasks.all()
        if is_duplicate:
            message = "One or more fields contain duplicates with our records, the rest has been updated."
        else:
            message = "Profile successfully updated"
        return render(request, 'main/profile.html', {
                "user": current_user,
                "tasks": tasks,
                "message": message
            })

#### MARKETPLACE MODULE ####
# Listings page
@login_required(login_url='/main/login')
def marketplace(request):
    redeemed = Reward.objects.filter(quantity = 0)
    return render(request, 'main/marketplace.html', {
        "listings": Reward.objects.all(),
        "redeemed": redeemed
    })

def add_to_cart(request):
    if request.method == "POST":
        reward = Reward.objects.get(pk=request.POST["listing_id"])
        current_user = CustomUser.objects.get(user=request.user)
        if current_user.points < reward.cost:
            return render(request, 'main/marketplace.html', {
                "message": "Insufficient points"
            })
        elif reward.quantity <= 0:
            return render(request, 'main/marketplace.html', {
                "message": "Sold out :("
            })
        else:
            pass

            
def view_cart(request):
    pass

def checkout(request):
    pass

#### TASK MODULE ####
# Tasks page
@login_required(login_url='/main/login')
def tasks(request):
    current_user = CustomUser.objects.get(user=request.user)
    to_do = Task.objects.filter(status="To do")
    in_progress = Task.objects.filter(status="In progress")
    completed = Task.objects.filter(status="Completed")
    return render(request, 'main/tasks.html', {
        "user": current_user,
        "to_do": to_do,
        "in_progress": in_progress,
        "completed": completed,
    })

@login_required(login_url='/main/login')
def edit_task(request):
     if request.method == "POST":
        task = Task.objects.get(pk=int(request.POST['task_id']))
        task.status = request.POST['task_status']
        task.save()
        return HttpResponseRedirect(reverse('main:tasks'))

#### AUTHENTICATION MODULE ####    
# logging in and out
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("main:index"))
        else:
            return render(request, 'main/login.html', {
                "message": "Incorrect username or password"
            })
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'main/login.html', {
        "message": "Logged out successfully"
    })