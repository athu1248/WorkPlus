
from django import forms
from .models import Documents, Project, Task, WorkGroup, WorkGroupUser

# form for creating new group
class NewWorkGroupForm(forms.ModelForm):
    class Meta:
        model = WorkGroup
        fields = ["groupName"]
        widgets = {
            "groupName": forms.TextInput(attrs={"placeholder": "Group Name...", "class": "form-control"}),
        }

# form for adding new user to group
class AddWorkGroupUserForm(forms.ModelForm):
    class Meta:
        model = WorkGroupUser
        fields = "__all__"
        widgets = {"work_group": forms.HiddenInput()}

# form for adding project to group
class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        
        widgets = {
            "project_name": forms.widgets.TextInput(attrs={"placeholder": "Project Name...", "class":"form-control"}),
            "project_description": forms.widgets.TextInput(attrs={"placeholder": "Project Description...", "class": "form-control"}),
            "work_group": forms.HiddenInput(),
            "status": forms.HiddenInput(),
        }
        """
        widgets = {
            "work_group": forms.HiddenInput()
        }
        """

# form for adding task to group
class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        #fields = ["task_name", "task_description", "work_group", "project"]
        #exclude = ("author",)
        widgets = {
            "task_name": forms.widgets.TextInput(attrs={"placeholder": "Task Name...", "class":"form-control"}),
            "task_description": forms.widgets.TextInput(attrs={"placeholder": "Task Description...", "class": "form-control"}),
            "project": forms.widgets.Select(attrs={"placeholder": "Task Description...", "class": "form-select", "aria-label": "Default select example"}),
            "author": forms.HiddenInput(),
            "work_group": forms.HiddenInput(),
            "status": forms.HiddenInput(),
        }

# form for uploading file to group
class AddFileForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = "__all__"
        widgets = {
            "work_group": forms.HiddenInput()
        }
