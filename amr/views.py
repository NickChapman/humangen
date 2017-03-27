from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from amr.forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages


MESSAGE_TAGS = {
    messages.constants.ERROR: 'danger'
}


def index(request):
    return render(request, 'amr/home.html')


def signup(request):
    if request.method == "POST":
        # Process their registration
        if request.POST.get('login', None):
            # They are trying to login
            pass
        elif request.POST.get('registration', None):
            # They are trying to register
            pass
        else:
            # They messed something up so just direct them back to this page so they can fix it
            messages.error(request, 'Something went wrong. Please try again.')
            return redirect('signup')
    else:
        # Return the registration form
        login_form = UserLoginForm()
        registration_form = UserRegistrationForm()
        return render(request, 'amr/signup.html', {
            'registration_form': registration_form,
            'login_form': login_form,
        })


def about(request):
    return render(request, 'amr/about.html')


def contact(request):
    return render(request, 'amr/contact.html')


def not_found(request):
    raise Http404("Page does not exist")
