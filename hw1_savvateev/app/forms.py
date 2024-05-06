import django.forms
from django.forms import inlineformset_factory
from django import forms
from django.contrib.auth.models import User
from django.db import models

from app.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username is None:
            raise forms.ValidationError('Please enter your username')
        user_from_db = User.objects.filter(username=username)
        if not user_from_db.exists():
            raise forms.ValidationError('This username does not exist')
        return username

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.filter(username=username)
        if user.exists():
            if not user[0].check_password(password):
                raise forms.ValidationError('Passwords do not match')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'nickname', 'password', 'confirm_password', 'avatar']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username is None:
            raise forms.ValidationError('Please enter your username')

        db_user = User.objects.filter(username=username)
        if db_user.exists():
            raise forms.ValidationError('This username already exists')
        return username

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        if password is None:
            raise forms.ValidationError('Please enter your password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        profile = Profile(
            user=user,
            nickname=self.cleaned_data.get('nickname'),
            avatar=self.cleaned_data.get('avatar'),
        )
        profile.save()
        return user


class ProfileForm(forms.ModelForm):
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['login', 'email', 'nickname', 'avatar']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

    def clean_login(self):
        old_username = self.request.user.get_username()
        username = self.cleaned_data.get('login')
        if username is None:
            raise forms.ValidationError('Please enter your username')

        db_user = User.objects.filter(username=username)
        if db_user.exists() and username != old_username:
            raise forms.ValidationError('This username already exists')
        return username

    def clean(self):
        super().clean()

    def save(self, commit=True):
        userProfile = Profile.profiles.get_by_username(self.request.user.username)
        userProfile.user.username = self.cleaned_data.get('login')
        userProfile.user.email = self.cleaned_data.get('email')
        userProfile.nickname = self.cleaned_data.get('nickname')
        userProfile.avatar = self.cleaned_data.get('avatar')
        userProfile.user.save()
        userProfile.save()
        return userProfile
