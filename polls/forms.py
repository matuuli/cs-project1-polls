from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    #these are here only for demonstration purposes, so we can see the password as we're typing it, we only need the class Meta for this part
    password1 = forms.CharField(
        label='Password',
        widget=forms.TextInput()
    )

    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.TextInput()
    )
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']