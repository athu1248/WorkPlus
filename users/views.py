from fitbit.models import FitBitUser
from django.forms.widgets import ClearableFileInput
from django.http import request, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from workgroups.models import WorkGroup, WorkGroupUser
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from workgroups.forms import NewWorkGroupForm
from fitbit.fitbitvars import getFitbitData

import uuid

# Create your views here.

# returns the home page of the website
def home(request):
    return render(request, "users/home.html", {})


# returns the sign up page and registers new user
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
         # redirect back to the user page with errors
         return render(request, 'users/register.html', {'form': form})
    form = UserRegisterForm()
    return render(request, "users/register.html", context={"form": form})


# returns user's personal profile dashboard upon login
@login_required
def profile(request, groupid = None):
    if request.method == "POST":
        if "removeGroup" in request.POST:
            getUUID = request.POST["removeGroup"]
            groupuuid = uuid.UUID(getUUID)
            workgroup = WorkGroup.objects.get(groupID=groupuuid)
            userToDelete = WorkGroupUser.objects.filter(work_group=workgroup).filter(user=request.user)
            userToDelete.delete()
            return redirect("profile")

        elif "createGroupSubmit" in request.POST:
            groupForm = NewWorkGroupForm(request.POST)
            if groupForm.is_valid():
                groupid = uuid.uuid4()

                workGroup = WorkGroup()
                workGroup.groupID = groupid
                workGroup.groupName = groupForm.cleaned_data["groupName"]
                workGroup.save()

                workGroup = WorkGroup.objects.get(groupID=groupid)

                # Add user who created the form to the new group as a leader
                workGroupUser = WorkGroupUser()
                workGroupUser.work_group = workGroup
                workGroupUser.user = request.user
                workGroupUser.userType = "leader"
                workGroupUser.save()        

        elif "changeProfileSubmit" in request.POST:
            profilePicForm = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if profilePicForm.is_valid:
                profilePicForm.save()

    if (request.user.is_authenticated):
        groups = getGroups(request.user)
        groupForm = NewWorkGroupForm()
        profilePicForm = ProfileUpdateForm()
        fitnessData = False
        if (FitBitUser.objects.filter(user_id = request.user).exists()):
            fitnessData = getFitbitData(request.user)
        return render(request, "users/profile.html", {"groups": groups, "createGroupForm": groupForm, "fitnessData": fitnessData, "changePicForm": profilePicForm,})

    return render(request, "users/home.html", {})

# displays all of the user's groups
def getGroups(user):
    groups = user.workgroupuser_set.all()
    contextGroups = []
    for group in groups:
        contextGroups.append({"groupName": group.work_group.groupName, "groupid":  str(group.work_group.groupID), "groupPic": group.work_group.groupPic})
    return contextGroups
