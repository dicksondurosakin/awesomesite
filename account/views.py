from django.shortcuts import redirect, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

from account.forms import UserRegistrationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


# This was just to know how login works i later django default class based view for login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'].lower(), password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('account:dashboard')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, "Username or password Incorrect")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user but avoids saving it yet
            # create  the object but don't commit yet 
            new_user = user_form.save(commit=False)
            # set the password, but you have to hash it unless it django wont save it
            new_user.set_password(user_form.cleaned_data['password2'])
            new_user.username = user_form.cleaned_data['username'].lower()
            # finally save it
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        try:
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST,
                                        files=request.FILES)
        except:
            profile_form = ProfileEditForm(instance=request.user,data=request.POST,
                                        files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile Updated Successfully")
        else:
            messages.error(request, "Error Updating Profile")
    else:
        user_form = UserEditForm(instance=request.user)
        try:
            profile_form = ProfileEditForm(instance=request.user.profile)
        except:
            profile_form = ProfileEditForm(instance=request.user)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
            'account/user/list.html',
            {'section': 'people',
            'users': users})
    
@login_required
def user_detail(request, username):
 user = get_object_or_404(User,
                        username=username,
                        is_active=True)
 return render(request,
                'account/user/detail.html',
                {'section': 'people',
                'user': user})