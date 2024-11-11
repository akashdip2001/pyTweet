from django import forms
from .models import Tweet # Import the Tweet model to modify everything of tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# What is form?
#From use to associate existing models with html input field and use the Django power.

# or May you create your own form without models. & data pass in views.py

# But in this case, we are using the existing model to create a form.
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo'] # names comes from the model.py
        # labels = {
        #     'text': 'Tweet',
        #     'photo': 'Photo'
        # }
        # widgets = {
        #     'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What is happening?'}),
        #     'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        # }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2') # names comes from the model.py
        