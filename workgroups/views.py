from users.models import Account
from django.contrib.auth.decorators import login_required
from workgroups.models import WorkGroupUser
from django.shortcuts import render
from django.contrib import messages
from django import forms
from .models import Chat, Documents, Project, Task, WorkGroup, WorkGroupUser
from .forms import AddFileForm, AddProjectForm, AddTaskForm, AddWorkGroupUserForm, AddWorkGroupUserForm, NewWorkGroupForm
import uuid
#from .forms import NewWorkGroupForm

# Create your views here.

# allows user to create new groups on their profile dashboard 
def newGroup(request):
    form = NewWorkGroupForm()
    if request.method == "POST":
        form = NewWorkGroupForm(request.POST)
        if form.is_valid():
            groupid = uuid.uuid4()

            workGroup = WorkGroup()
            workGroup.groupID = groupid
            workGroup.groupName = form.cleaned_data["groupName"]
            workGroup.save()

            workGroup = WorkGroup.objects.get(groupID=groupid)

            workGroupUser = WorkGroupUser()
            workGroupUser.work_group = workGroup
            workGroupUser.user = request.user
            workGroupUser.userType = "leader"
            workGroupUser.save()

            return render(request, "users/home.html", {})

    return render(request, "workgroups/new-group.html", {"form": form})

# allows users to perform various operations on their group's dashboard
@login_required
def group(request, groupid):
    groupuuid = uuid.UUID(groupid)
    if WorkGroup.objects.filter(groupID=groupuuid).exists():
        workGroup = WorkGroup.objects.get(groupID=groupuuid)
        if(request.user.workgroupuser_set.filter(work_group=workGroup).exists()):
            if request.method == "POST":
                if "addNewUserSubmit" in request.POST:
                    formAddUser = AddWorkGroupUserForm(request.POST)
                    if formAddUser.is_valid():
                        formAddUser.save()
                        workGroup = formAddUser.cleaned_data["work_group"]      #adding user to group

                elif "addNewProjectSubmit" in request.POST:
                    formAddProject = AddProjectForm(request.POST)
                    if formAddProject.is_valid():
                        formAddProject.save()
                        workGroup = formAddProject.cleaned_data["work_group"]   #adding project to dashboard

                elif "addNewTaskSubmit" in request.POST:
                    formAddTask = AddTaskForm(request.POST)
                    if formAddTask.is_valid():
                        formAddTask.save()
                        workGroup = formAddTask.cleaned_data["work_group"]     #adding task to dashboard

                elif "addFileSubmit" in request.POST:
                    formAddFile = AddFileForm(request.POST, request.FILES)
                    if formAddFile.is_valid():
                        formAddFile.save()
                        workGroup = formAddFile.cleaned_data["work_group"]     #uploading file to dashboard
                    else:
                        # FileError here
                        pass
                
                elif "removeUser" in request.POST:
                    name = request.POST["removeUser"]
                    userToDelete = Account.objects.get(username=name)
                    workgroup = WorkGroup.objects.get(groupID=groupuuid)
                    users = WorkGroupUser.objects.filter(work_group = workgroup)
                    users.get(user=userToDelete).delete()                      #removing user from group

                elif "removeProject" in request.POST:
                    projectid = request.POST["removeProject"]
                    Project.objects.get(id = projectid).delete()               #deleting project from dashboard 
                
                elif "removeTask" in request.POST:
                    taskid = request.POST["removeTask"]
                    Task.objects.get(id=taskid).delete()                       #deleting task from dashboard
                
                elif "completeProjectSubmit" in request.POST:
                    projectid = request.POST["completeProjectSubmit"]
                    projectToComplete = Project.objects.get(id=projectid)
                    projectToComplete.status = "complete"
                    projectToComplete.save()                                   #complete project in dashboard     

                elif "completeTaskSubmit" in request.POST:
                    taskid = request.POST["completeTaskSubmit"]
                    taskToComplete = Task.objects.get(id=taskid)
                    taskToComplete.status = "complete"
                    taskToComplete.save()                                      #complete task in dashboard

                
    
            members, msgs, projects, tasks, files, formAddUser, formAddProject, formAddTask, formAddFile, usertype = getAllWorkGroupData(workGroup, request.user)
            return render(request, "workgroups/group-home.html", {
                "groupuuid": groupuuid,
                "user": request.user,
                "groupName": workGroup.groupName,
                "groupPic": workGroup.groupPic,
                "members":  members,
                "msgs": msgs,
                "projects": projects,
                "tasks": tasks,
                "files": files,
                "formAddUser": formAddUser,
                "formAddProject": formAddProject,
                "formAddTask": formAddTask,
                "formAddFile": formAddFile,
                "usertype": usertype,
            })

    return render(request, "home.html", {})

# get various data related to your current group
def getAllWorkGroupData(workGroup, user):
    
    # get the role of your group members - leader/member
    groupUsers = WorkGroupUser.objects.filter(work_group=workGroup)
    members = {}
    for groupUser in groupUsers:
        members[groupUser.user.username] = groupUser.userType

    # get all chats within a group
    msgs = []
    chatObjs = Chat.objects.filter(work_group=workGroup).order_by("dateCreated")
    for chatObj in chatObjs:
        msgs.append([chatObj.author.username, chatObj.message])

    # get all projects of a group 
    projects = []
    projectObjs = Project.objects.filter(work_group=workGroup).order_by("-status")
    for projectObj in projectObjs:
        projects.append({"projectName":projectObj.project_name, "projectDescription": projectObj.project_description, "projectID": projectObj.id, "projectStatus": projectObj.status})
    
    # get all tasks of a group 
    tasks = []
    taskObjs = Task.objects.filter(project__in=projectObjs).order_by("-status")
    for taskObj in taskObjs:
        tasks.append({"taskName": taskObj.task_name, "taskDescription": taskObj.task_description, "author": taskObj.author.username, "projectName": taskObj.project.project_name, "taskID": taskObj.id, "taskStatus": taskObj.status})

    # get all files uploaded by a group 
    files = []
    fileObjs = Documents.objects.filter(work_group=workGroup)
    for fileObj in fileObjs:
        files.append({"file": fileObj.file})

    # add user to the current group
    formAddUser = AddWorkGroupUserForm()
    formAddUser.initial["work_group"] = workGroup

    # add project to the current group
    formAddProject = AddProjectForm()
    formAddProject.initial["work_group"] = workGroup
    
    # add task to the current group
    formAddTask = AddTaskForm()
    formAddTask.fields["project"] = forms.ModelChoiceField(queryset=projectObjs)
    formAddTask.initial["work_group"] = workGroup
    formAddTask.initial["author"] = user

    # upload file to the current group
    formAddFile = AddFileForm()
    formAddFile.initial["work_group"] = workGroup

    return members, msgs, projects, tasks, files, formAddUser, formAddProject, formAddTask, formAddFile, members[user.username]
