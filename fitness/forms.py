from django import forms
from .models import quizUser, runImage


# form for accepting user's daily nike run challenge screenshot
class runImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = runImage
        fields = "__all__"
        widgets = {
            "user": forms.HiddenInput()
            }

# form for accepting user's trivia of the day answer
class quizUserForm(forms.ModelForm):
    answer = forms.ChoiceField(widget=forms.RadioSelect)
    """Form for the image model"""
    class Meta:
        model = quizUser
        fields = "__all__"
        widgets = {
            "user": forms.HiddenInput(),
            "question": forms.HiddenInput(),
            "correct": forms.HiddenInput(),
        }

