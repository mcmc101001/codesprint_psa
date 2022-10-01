from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    #authentication
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    #social
    path('users/', views.users, name='users'),
    path('users/<int:user_id>', views.user_profile, name='user_profile'),
    path('follow', views.follow, name='follow'),
    path('modify_request', views.modify_request, name='modify_request'),
    #profile
    path('profile', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('update_profile', views.update_profile, name='update_profile'),
    #tasks
    path('tasks', views.tasks, name="tasks"),
    path('edit_task', views.edit_task, name="edit_task"),
    #tasks
    path('marketplace', views.marketplace, name="marketplace"),
    path('redeem_reward', views.redeem_reward, name="redeem_reward"),
]