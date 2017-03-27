from django.shortcuts import render
from django.http import HttpResponse
from amr.forms import UserRegistrationForm


def index(request):
    return HttpResponse("Hello world!")


def signup(request):
    if request.method == "POST":
        # Process their registration
        pass
    else:
        # Return the registration form
        form = UserRegistrationForm()
        return render(request, 'amr/signup.html', {'form': form})