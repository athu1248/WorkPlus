from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import fields

from .models import Profile, Account
from .widgets import XDSoftDateTimePickerInput

# form for user sign up
class UserRegisterForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=AdminDateWidget())
    class Meta:
        model = Account
        fields = ["username", "email", "first_name", "last_name",
                  "date_of_birth", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(),
            "email": forms.EmailInput(),
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
        }

# form for updating user's name and email in their profile
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ["email", "first_name", "last_name"]

# form for updating user's profile picture
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
