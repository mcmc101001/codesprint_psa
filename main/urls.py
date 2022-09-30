from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('profile', views.profile, name='profile'),
    path('tasks', views.tasks, name="tasks"),
    path('edit_task', views.edit_task, name="edit_task")
]