from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            cuser = form.cleaned_data.get('username')
            cmuser= User.objects.get(username=cuser)
            nprofile= Profile(user=cmuser)
            nprofile.save()
            age = form.cleaned_data.get('age')
            messages.success(request, f'Your account has been created. Now you can login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
@login_required
def profile(request):
    if request.method=="POST":
        u_form = UserUpdateForm(request.POST, instance= request.user)
        p_form = profileUpdateForm(request.POST, request.FILES, instance= request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile Updated successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm( instance= request.user)
        p_form = profileUpdateForm( instance= request.user.profile)

    context = {
        'u_form':u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context )