from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from amr.forms import UserRegistrationForm, UserLoginForm

MESSAGE_TAGS = {
    messages.constants.ERROR: 'danger'
}


def index(request):
    return render(request, 'amr/home.html')


def signup(request):
    login_form = UserLoginForm()
    registration_form = UserRegistrationForm()
    if request.method == "POST":
        # Process their registration
        if request.POST.get('login', None):
            login_form = UserLoginForm(request.POST)
            if login_form.is_valid():
                user = authenticate(username=login_form.cleaned_data['email'], password=login_form.cleaned_data['email'])
                if user is not None:
                    login(request, user)
                    return redirect('home')
        elif request.POST.get('registration', None):
            # They are trying to register
            registration_form = UserRegistrationForm(request.POST)
            if registration_form.is_valid():
                if registration_form.cleaned_data['email'] == registration_form.cleaned_data['confirm_email'] and registration_form.cleaned_data['password'] == registration_form.cleaned_data['confirm_password']:
                    user = User.objects.create_user(registration_form.email, registration_form.email, registration_form.password)
                    login(request, user)
                    return redirect('home')
        else:
            # They messed something up so just direct them back to this page so they can fix it
            messages.error(request, 'Something went wrong. Please try again.')
            return redirect('signup')
    # This is the default fall through area
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
