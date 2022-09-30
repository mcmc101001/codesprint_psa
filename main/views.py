import re
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import CustomUser, Task

# Main page
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("main:login"))
    else:
        return render(request, "main/index.html")

# Profile page
@login_required(login_url='/main/login')
def profile(request):
    current_user = CustomUser.objects.get(user=request.user)
    tasks = current_user.tasks.all()
    return render(request, 'main/profile.html', {
        "user": current_user,
        "tasks": tasks
    })

# Tasks page
@login_required(login_url='/main/login')
def tasks(request):
    current_user = CustomUser.objects.get(user=request.user)
    tasks = current_user.tasks.all()
    return render(request, 'main/tasks.html', {
        "user": current_user,
        "tasks": tasks
    })

@login_required(login_url='/main/login')
def edit_task(request):
     if request.method == "POST":
        task = Task.objects.get(pk=int(request.POST['task_id']))
        task.status = request.POST['task_status']
        task.save()
        return HttpResponseRedirect(reverse('main:tasks'))
    
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