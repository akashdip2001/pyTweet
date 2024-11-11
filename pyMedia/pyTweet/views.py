from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegisterForm #TweetForm: Recheck --> app/ forms.py --> class TweetForm(forms.ModelForm):
from django.shortcuts import get_object_or_404, redirect # get_object_or_404 is used to get the object from the model or return 404 error
from django.contrib.auth.decorators import login_required # login_required is used to check if the user is logged in or not
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at') # Get all the tweets from the database and order by created_at
    return render(request, 'tweet_list.html', {'tweets': tweets}) # Pass the tweets to the template

@login_required # This decorator is used to check if the user is logged in or not
def tweet_create(request):
    if request.method == 'POST': # Check if the request method is POST
        form = TweetForm(request.POST, request.FILES) # Create a form with the request data
        if form.is_valid(): # Check if the form is valid
            tweet = form.save(commit=False) # Don't Save the form data to the database, just hold it in the variable
            tweet.user = request.user # Set the user of the tweet to the current user
            tweet.save() # Now Save the tweet to the database
            return redirect('tweet_list') # Redirect to the tweet list page
    else:       
        form = TweetForm() # Create a new form
    return render(request, 'tweet_form.html', {'form': form}) # Pass the form to

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user) # Get the tweet object from the database, user = request.user --> only login user can edit the tweet.
    if request.method == 'POST': 
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet) # Create a form with the tweet data, instance=tweet is used to populate the form with the tweet data
    return render(request, 'tweet_form.html', {'form': form}) # Pass the form to

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user) # Get the tweet object from the database, user = request.user --> only login user can delete the tweet.
    if request.method == 'POST':
        tweet.delete() # Delete the tweet
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet}) # Pass the tweet to the template


# create views to user registration and login
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Securely set the password
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})