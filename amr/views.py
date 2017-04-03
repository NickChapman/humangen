from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
from amr.forms import UserRegistrationForm, UserLoginForm, AmrGenerationForm
from amr.models import *


def index(request):
    return render(request, 'amr/index.html')


def signup(request):
    login_form = UserLoginForm()
    registration_form = UserRegistrationForm()
    if request.method == "POST":
        # Process their registration
        if request.POST.get('login', None):
            login_form = UserLoginForm(request.POST)
            if login_form.is_valid():
                user = authenticate(username=login_form.cleaned_data['email'],
                                    password=login_form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    if request.GET.get('next', None) is None:
                        return redirect('index')
                    else:
                        return redirect(request.GET.get('next'))
                else:
                    messages.error(request, "Invalid email/password combination")
        elif request.POST.get('registration', None):
            # They are trying to register
            registration_form = UserRegistrationForm(request.POST)
            if registration_form.is_valid():
                if registration_form.cleaned_data['email'] != registration_form.cleaned_data['confirm_email']:
                    messages.error(request, "Email addresses do not match")
                    return redirect('signup')
                if registration_form.cleaned_data['password'] != registration_form.cleaned_data['confirm_password']:
                    messages.error(request, "Passwords do not match")
                    return redirect('signup')
                if User.objects.filter(username=registration_form.cleaned_data['email']).count() != 0:
                    messages.error(request, "Email is already registered")
                    return redirect('signup')
                user = User.objects.create_user(registration_form.cleaned_data['email'],
                                                registration_form.cleaned_data['email'],
                                                registration_form.cleaned_data['password'])
                login(request, user)
                if request.GET.get('next', None) is None:
                    return redirect('index')
                else:
                    return redirect(request.GET.get('next'))
        else:
            # They messed something up so just direct them back to this page so they can fix it
            messages.error(request, 'Something went wrong. Please try again.')
            return redirect('signup')
    # This is the default fall through area
    return render(request, 'amr/signup.html', {
        'registration_form': registration_form,
        'login_form': login_form,
    })


def signout(request):
    if request.user.is_authenticated():
        logout(request)
        messages.success(request, 'Successfully logged out')
    return redirect('index')


def contact(request):
    return render(request, 'amr/contact.html')


@login_required
def generate(request):
    amr_form = AmrGenerationForm()
    if request.method == "POST":
        # They are submitting a generation
        amr_form = AmrGenerationForm(request.POST)
        if amr_form.is_valid():
            amr = AmrEntry.objects.get(id=amr_form.cleaned_data['amr_id'])
            generation = Generation(amr=amr, generation=amr_form.cleaned_data['generation'], user=request.user)
            generation.save()
            messages.success(request, 'Generation saved. Thanks! Want to do another?')
            return redirect('generate')
    # Select a random AMR for them to generate
    amr_ids = AmrEntry.objects.values_list('id', flat=True)
    random_id = random.sample(list(amr_ids), 1)
    amr = AmrEntry.objects.get(id__in=random_id)
    amr_form.amr_id = amr.id
    return render(request, 'amr/generate.html', {'amr': amr, 'amr_form': amr_form})


def not_found(request):
    raise Http404("Page does not exist")
