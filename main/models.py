from email.policy import default
from django.db import models

from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.
class Task(models.Model):
    
    STATUS = (
        ('To do', 'To do'),
        ('In progress', 'In progress'),
        ('Completed', 'Completed'),
    )
    name = models.CharField(max_length = 64)
    description = models.TextField("Description", max_length=600, default='', blank=True)
    points_granted = models.IntegerField()
    status = models.CharField(max_length=100, choices=STATUS, default='To do')
    
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
    requestor = models.ForeignKey(CustomUser, related_name="from_request", on_delete=models.CASCADE)
    requested = models.ForeignKey(CustomUser, related_name="to_request", on_delete=models.CASCADE)

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name="from_follow", on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name="to_follow", on_delete=models.CASCADE)
    date = models.DateField()

class Reward(models.Model):
    name = models.CharField(max_length = 64)
    description = models.TextField("Description", max_length=600, default='', blank=True)
    quantity = models.IntegerField()
    cost = models.IntegerField()
    
    def __str__(self):
        return self.name