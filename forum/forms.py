__author__ = 'medina'

from django.forms import ModelForm
from django import forms
from .models import *



class UserForm(forms.Form):

    username = forms.CharField(min_length=5)
    email = forms.EmailField()
    password = forms.CharField(min_length=5, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('The username "{}" is already taken'.format(username))
        return username

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('The e-mail "{}" is already taken'.format(email))
        return email

    def clean_password_confirmation(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password_confirmation']
        if password != password2:
            raise forms.ValidationError('Password fields do not match')
        return password2


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        exclude=['no_of_threads']

class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        exclude=['topic','no_of_messages']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude=['thread', 'user']

class AvatarChangeForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']
