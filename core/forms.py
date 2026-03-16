# Import Form libary
from django import forms
# Import models
from .models import UserContact
# Import Django Users model & Forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# User contact form
class UserContactForm(forms.ModelForm):
    class Meta:
        # Model Name
        model = UserContact
        #Form Fields
        fields = [
            'first_name',
            'last_name',
            'email',
            'message'
        ]

# Create user form
class CreateUserForm(UserCreationForm ,forms.ModelForm):
     class Meta:
        # Model name
        model = User
        # Form Fields
        fields = [
            'first_name',
            'last_name',
            'username',
            'email'
        ]