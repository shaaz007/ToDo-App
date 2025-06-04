from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.dateparse import parse_datetime
from .models import Post

# Utility function to validate file size which is being uploaded by the user. File size is restricted to 5 MB.
def validate_file_size(value):
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError("File size should not exceed 5 MB. Please upload a valid file.")


# User registration form with the fields like full name, username, email and password.
class CustomUserCreationForm(UserCreationForm):
    # name and email address restricted with the max length and also considered to be an mandatory fields
    name = forms.CharField(
        max_length=70,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Full Name"
    )
    email = forms.EmailField(
        max_length=70,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Email Address"
    )

# Input type for the fields like textinput and password input are mentioned
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


# The date and time filter which is added during the todo task addition and modifications. The format of how date and time needs to be stored is mentioned below
class TodoForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'placeholder': 'Select deadline',
        }),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

# The Todo form and all the fields which can be configured by user is listed and their input types in form are listed, like the title has the 'textInput', which can be selected from drop down are listed as 'forms.Select'. File attachments as 'forms.FileInput'
    class Meta:
        model = Post
        fields = [
            'title',
            'description',
            'deadline',
            'category',
            'priority',
            'completed',
            'recurrence',
            'attachment',
            'progress',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'recurrence': forms.Select(attrs={'class': 'form-select'}),
            'progress': forms.Select(attrs={'class': 'form-select'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }

# the provided date and time will be checked with the current time, if the date is found to be lesser than the current time, appropriate error prompt would be displayed.
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < now():
            raise ValidationError("The deadline is incorrect. Please provide the date and time in future")
        return deadline

# The function which checks the file size of the attachment
    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachment')
        if attachment:
            validate_file_size(attachment)
        return attachment
