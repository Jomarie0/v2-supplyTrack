from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    
    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        
        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirmation
