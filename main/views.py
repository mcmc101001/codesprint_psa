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
    top_users = CustomUser.objects.order_by('-points')[:3]
    if CustomUser.objects.filter(birthday__day = datetime.now().date().day, birthday__month = datetime.now().date().month):
        birthday_boy = CustomUser.objects.filter(birthday__day = datetime.now().date().day, birthday__month = datetime.now().date().month)
        return render(request, "main/index.html", {
        "following": following,
        "requests": requests,
        "top_users": top_users,
        "birthday_boy": birthday_boy,
    })
    return render(request, "main/index.html", {
        "following": following,
        "requests": requests,
        "top_users": top_users
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
    to_do = user.tasks.filter(status="To do")
    in_progress = user.tasks.filter(status="In progress")
    completed = user.tasks.filter(status="Completed")
    return render(request, 'main/user_profile.html', {
        "user": user,
        "to_do": to_do,
        "in_progress": in_progress,
        "completed": completed,
    })

#### PROFILE MODULE ####
# Profile page
@login_required(login_url='/main/login')
def profile(request):
    current_user = CustomUser.objects.get(user=request.user)
    to_do = current_user.tasks.filter(status="To do")
    in_progress = current_user.tasks.filter(status="In progress")
    completed = current_user.tasks.filter(status="Completed")
    return render(request, 'main/profile.html', {
        "user": current_user,
        "to_do": to_do,
        "in_progress": in_progress,
        "completed": completed,
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
        to_do = current_user.tasks.filter(status="To do")
        in_progress = current_user.tasks.filter(status="In progress")
        completed = current_user.tasks.filter(status="Completed")
        if is_duplicate:
            message = "One or more fields contain duplicates with our records, the rest has been updated."
        else:
            message = "Profile successfully updated"
        return render(request, 'main/profile.html', {
                "user": current_user,
                "to_do": to_do,
                "in_progress": in_progress,
                "completed": completed,
                "message": message
            })

#### MARKETPLACE MODULE ####
# Listings page
@login_required(login_url='/main/login')
def marketplace(request):
    if request.method == "POST":
        redeemed = Reward.objects.filter(quantity = 0)
        reward = Reward.objects.get(pk=request.POST["listing_id"])
        current_user = CustomUser.objects.get(user=request.user)
        if current_user.points < reward.cost:
            return render(request, 'main/marketplace.html', {
                "listings": Reward.objects.all(),
                "redeemed": redeemed,
                "message": "Insufficient credits :("
            })
        elif reward.quantity <= 0:
            return render(request, 'main/marketplace.html', {
                "listings": Reward.objects.all(),
                "redeemed": redeemed,
                "message": "Sold out :("
            })
        if Cart.objects.filter(user=current_user, reward=reward):
            cart = Cart.objects.get(user=current_user, reward=reward)
            cart.count = cart.count + 1
            cart.save()
        else: 
            user_cart = Cart(user=current_user, reward=reward, count=1)
            user_cart.save()
        return render(request, 'main/marketplace.html', {
                "listings": Reward.objects.all(),
                "redeemed": redeemed,
                "message": "Added to cart!"
            })
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
        if Cart.objects.filter(user=current_user, reward=reward):
            cart = Cart.objects.get(user=current_user, reward=reward)
            cart.count = cart.count + 1
            cart.save()
        else: 
            user_cart = Cart(user=current_user, reward=reward, count=1)
            user_cart.save()
        return HttpResponseRedirect(reverse('main:marketplace'))

            
def view_cart(request):
    current_user = CustomUser.objects.get(user=request.user)
    cart = Cart.objects.filter(user=current_user)
    cost = 0
    for cart_item in cart:
        cost += cart_item.reward.cost*cart_item.count
    return render(request, 'main/cart.html', {
        "rewards": cart,
        "total_cost": cost,
    })

def edit_quantity(request):
    if request.method == 'POST':
        cart = Cart.objects.get(pk=request.POST["cart_id"])
        try:
            outcome = request.POST["add"]
        except:
            outcome = "minus"
        if outcome == "Add":
            cart.count += 1
        else:
            cart.count -= 1
        cart.save()
        if cart.count == 0:
            cart.delete()
        return HttpResponseRedirect(reverse('main:view_cart'))

def checkout(request):
    if request.method == "POST":
        current_user = CustomUser.objects.get(user=request.user)
        cart = Cart.objects.filter(user=current_user)
        cost = int(request.POST["total_cost"])
        is_successful = True
        if current_user.points < cost:
            message = "Insufficient points!"
            return HttpResponseRedirect(reverse('main:view_cart'))
        for cart_item in cart:
            if cart_item.count > cart_item.reward.quantity:
                message = "Unable to redeem one or more items due to lack of stock!"
                cost = cost - cart_item.count*cart_item.reward.cost
                is_successful = False
            else: 
                cart_item.reward.quantity = cart_item.reward.quantity - cart_item.count
                cart_item.reward.save()
                cart_item.delete()
        current_user.points = current_user.points - cost
        current_user.save()
        if is_successful:
            message = "Successfully checked out!"
        redeemed = Reward.objects.filter(quantity = 0)
    return render(request, 'main/marketplace.html', {
        "listings": Reward.objects.all(),
        "redeemed": redeemed,
        "message": message,
    })
        

#### TASK MODULE ####
# Tasks page
@login_required(login_url='/main/login')
def tasks(request):
    to_do = Task.objects.filter(status="To do")
    in_progress = Task.objects.filter(status="In progress")
    completed = Task.objects.filter(status="Completed")
    return render(request, 'main/tasks.html', {
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