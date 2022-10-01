from django.contrib import admin

from . models import CustomUser, Task, Reward, Follow

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Follow)
admin.site.register(Task)
admin.site.register(Reward)