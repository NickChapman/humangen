from django.shortcuts import render
from django.http import HttpResponse, Http404
from amr.forms import UserRegistrationForm


def index(request):
    return render(request, 'amr/home.html')


def signup(request):
    if request.method == "POST":
        # Process their registration
        pass
    else:
        # Return the registration form
        form = UserRegistrationForm()
        return render(request, 'amr/signup.html', {'form': form})


def about(request):
    return render(request, 'amr/about.html')


def contact(request):
    return render(request, 'amr/contact.html')


def not_found(request):
    raise Http404("Page does not exist")
