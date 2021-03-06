from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import (UserLoginForm, UserRegistrationForm, ProfileForm,
                            UserForm)
from accounts.models import Profile
from django.http import HttpResponse, HttpResponseRedirect


@login_required
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out")
    return redirect(reverse('index'))


def login(request):
    """Return a login page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Your username or password is incorrect")
    else:
        login_form = UserLoginForm()
    return render(request, "accounts/login.html", {"login_form": login_form})


def registration(request):
    """Render the registration page"""

    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered")
                return redirect(reverse('index'))
            else:
                messages.error(request, "Unable to register your account at this time")
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'accounts/registration.html', {'registration_form': registration_form})


def user_profile(request, id):
    """The user's profile page"""
    user = get_object_or_404(User, pk=id)
    profile = get_object_or_404(Profile, user=id)
    return render(request, 'accounts/profile.html', {"profile": profile, "user": user})


@login_required
def edit_profile(request, id):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        # Check if new email address and username are unique for the site.
        not_unique = False
        if "email" in user_form.changed_data or "username" in user_form.changed_data:
            if "email" in user_form.changed_data:
                form_email = request.POST['email']
                # Search for suggested email address in existing db.
                filter_emails = User.objects.filter(email=form_email)
                for filter_email in filter_emails:
                    if filter_email.id != request.user.id:
                        # If email address exists already change variable to True
                        not_unique = True
                        # return a message informing user that this is unavailable
                        messages.error(request, "Email address is already registered, please choose another.")
                        # redirect ot edit_profile
                        return redirect(reverse('edit_profile', kwargs={'id': id}))

            if "username" in user_form.changed_data:
                form_username = request.POST['username']
                # Search for suggested username in existing db.
                filter_usernames = User.objects.filter(username=form_username)

                for filter_username in filter_usernames:
                    if filter_username.id != request.user.id:
                        # If username exists already change variable to True
                        not_unique = True
                        # return a message informing user that this is unavailable
                        messages.error(request, "Username is not available, please choose another.")
                        # return to the edit profile page
                        return redirect(reverse('edit_profile', kwargs={'id': id}))

        # if all form are valid and username/email are unique update profile
        if user_form.is_valid() and profile_form.is_valid() and not_unique is False:
            user_form.save()
            profile = profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(profile.get_absolute_url())
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form})


    
        

    