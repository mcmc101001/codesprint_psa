from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Value
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import CustomUser, Request, Task, Reward, User, Follow, Cart

from datetime import datetime

@login_required(login_url='/main/login')
def cart_count(request):
    current_user = CustomUser.objects.get(user=request.user)
    cart_count = Cart.objects.filter(user=current_user).count()
    return {
        'cart_count' : cart_count
    }