from django.contrib import admin

from . models import CustomUser, Task, Reward, Follow, Request, Cart

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Follow)
admin.site.register(Task)
admin.site.register(Reward)
admin.site.register(Request)
admin.site.register(Cart)