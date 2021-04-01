import uuid
from django.db import models
from django.contrib.auth.models import Group, User
from users.models import Account
import django.utils.timezone as datetime

# Create your models here.

# stores all group details
class WorkGroup(models.Model):
    groupID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    groupName = models.TextField(max_length=64, unique=False)
    date_created = models.DateField(default=datetime.now)
    groupPic = models.ImageField(default="default.png", upload_to="group_pics")

    def __str__(self):
        return str(self.groupID) + " " + self.groupName

# stores all group-specifc user details
class WorkGroupUser(models.Model):
    work_group = models.ForeignKey(WorkGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    userType = models.TextField(choices=(("member", "member"), ("leader", "leader")), unique=False)

    def __str__(self):
        return self.user.username + " " + self.work_group.groupName

# stores all project details uploaded to dashboard
class Project(models.Model):
    project_name = models.TextField(max_length=50, blank=True, null=True, unique=False)
    project_description = models.TextField(max_length=100, blank=True, null=True, unique=False)
    work_group = models.ForeignKey(WorkGroup, on_delete=models.CASCADE)
    status = models.TextField(choices=(("completed", "completed"), ("not completed", "not completed")), default="not completed")

    def __str__(self):
        return self.project_name + " " + self.work_group.groupName

# stores all project details uploaded to dashboard
class Task(models.Model):
    task_name = models.TextField(max_length=50, blank=True, null=True, unique=False)
    task_description = models.TextField(max_length=250, blank=True, null=True, unique=False)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    work_group = models.ForeignKey(WorkGroup, on_delete=models.CASCADE, null=True)
    status = models.TextField(choices=(("completed", "completed"), ("not completed", "not completed")), default="not completed")

    def __str__(self):
        return self.task_name + " " + self.author.username + " " + self.project.project_name

# stores all chat details within a group
class Chat(models.Model):
    message = models.TextField(max_length=250)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    work_group = models.ForeignKey(WorkGroup, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(default=datetime.now)

# stores all files uploaded to the dashboard
class Documents(models.Model):
    file = models.FileField(upload_to='documents/')
    work_group = models.ForeignKey(WorkGroup, on_delete=models.CASCADE)
