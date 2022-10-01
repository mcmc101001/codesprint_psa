from email.policy import default
from django.db import models

from django.contrib.auth.models import User

import datetime

# Create your models here.
class Task(models.Model):
    
    STATUS = (
        ('Incomplete', 'Incomplete'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )
    name = models.CharField(max_length = 64)
    points_granted = models.IntegerField()
    status = models.CharField(max_length=100, choices=STATUS, default='Incomplete')
    
    def __str__(self):
        return self.name
    

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DEPARTMENT = (
        ('Operations', 'Operations'),
        ('Infocomm technology', 'Infocomm technology'),
        ('Engineering', 'Engineering'),
        ('Corportate', 'Corporate')
    )
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, choices=DEPARTMENT)
    description = models.TextField("Description", max_length=600, default='', blank=True)
    points = models.IntegerField(default=0)
    tasks = models.ManyToManyField(Task, blank=True, related_name='users')

    def __str__(self):
        return self.user.username

class Request(models.Model):
    requestor = models.OneToOneField(CustomUser, related_name="request", on_delete=models.CASCADE)
    requested = models.OneToOneField(CustomUser, related_name="requested_by", on_delete=models.CASCADE)

class Follow(models.Model):
    follower = models.OneToOneField(CustomUser, related_name="follow", on_delete=models.CASCADE)
    following = models.OneToOneField(CustomUser, related_name="followed_by", on_delete=models.CASCADE)
    datetime = models.DateTimeField()

class Reward(models.Model):
    name = models.CharField(max_length = 64)
    description = models.TextField("Description", max_length=600, default='', blank=True)
    quantity = models.IntegerField()
    cost = models.IntegerField()