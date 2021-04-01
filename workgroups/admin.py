from django.contrib import admin
from .models import Documents, WorkGroup, WorkGroupUser, Project, Task, Chat

# Register your models here.
admin.site.register(WorkGroup)
admin.site.register(WorkGroupUser)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Chat)
admin.site.register(Documents)
