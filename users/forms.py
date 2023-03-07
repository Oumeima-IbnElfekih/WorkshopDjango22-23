from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import *
class LoginForm(forms.ModelForm):
    class Meta:
        model=Person
        fields=['username','password']
    password=forms.ChoiceField(widget=forms.PasswordInput())
class RegisterForm(UserCreationForm):
    class Meta:
        model=get_user_model() 
        fields=['cin','username','first_name','last_name','email','password1','password2']
    
    def save(self, commit=True):
        return super(RegisterForm,self).save(commit)