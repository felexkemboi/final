from django import forms
from .models import *




class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [

            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'

        ]


class messageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [

            'To',
            'From',
            'subject',
            'body'

        ]