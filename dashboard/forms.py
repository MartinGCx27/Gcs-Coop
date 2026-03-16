# Import Form libary
from django import forms
# Import User model
from django.contrib.auth.models import User
# Import .models
# from .models import InformationIssue

from core.models import GcsServices

# Update password user
class UpdatePassUser(forms.ModelForm):
    class Meta:
        # Model name
        model = User
        # Form fields
        fields = [
            'first_name',
            'last_name',
            'username',
            'email'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Create services form
class CreateServiceForm(forms.ModelForm):
    image_service = forms.ImageField()
    class Meta:
        model = GcsServices
        fields = [
            'title',
            'description',
            'image_service'
        ]
# Update services form
class UpdateServiceForm(forms.ModelForm):
    image_service = forms.ImageField()
    class Meta:
        model = GcsServices
        fields = [
            'title',
            'description',
            'image_service',
            'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image_service': forms.ImageField,
            'status': forms.Select(attrs={'class': 'form-control'})
        }