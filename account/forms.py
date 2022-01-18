from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import fields
from .models import Profile

class LoginForm(forms.Form):
    username =  forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name','email')
    
    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise ValidationError("Email already exist")
        return cd['email']

    def clean_username(self):
        cd = self.cleaned_data
        # print(cd)
        # print(User.objects.filter(username=cd['username']))
        if User.objects.filter(username=cd['username']).exists():
            raise ValidationError("User already exists")
        return cd['username']
    
    def clean_password2(self):
        cd = self.cleaned_data
        # print(cd)
        if cd['password'] != cd['password2']:
            raise ValidationError('password don\'t match')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')
    
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')