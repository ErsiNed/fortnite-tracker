from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, EditUserForm, EditUserProfileForm
from .models import UserProfile


# ─── Registration / Authentication ────────────────────────────────

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


# ─── Profile Views ────────────────────────────────────────────────

@login_required
def profile_view(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    return render(request, 'profile.html', {
        'user': user,
        'profile': profile
    })


# ─── Profile Edit ─────────────────────────────────────────────────

@login_required
def edit_profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = EditUserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = EditUserForm(instance=user)
        profile_form = EditUserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# ─── Profile Deletion ─────────────────────────────────────────────

@login_required
def delete_profile_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log the user out before deleting
        user.delete()
        return redirect('home')
    return render(request, 'delete_profile.html')