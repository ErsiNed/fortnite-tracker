from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import UserRegisterForm, EditUserForm, EditUserProfileForm
from .models import UserProfile


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('profile')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {
        'form': form,
        'title': 'Register'
    })


@login_required
def profile_view(request):
    user = request.user
    profile = UserProfile.objects.get_or_create(user=user)[0]
    vbucks_summary = user.get_vbucks_summary()

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'vbucks_summary': vbucks_summary,
        'title': 'Your Profile'
    })


@login_required
def edit_profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = EditUserProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        user_form = EditUserForm(instance=user)
        profile_form = EditUserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Edit Profile'
    })


@login_required
def delete_profile_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect(reverse_lazy('vbucks_tracker:home'))

    return render(request, 'delete_profile.html', {
        'title': 'Delete Account'
    })