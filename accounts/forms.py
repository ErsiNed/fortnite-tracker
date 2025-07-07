from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()


# ───  Registration Form ─────────────────────────────────────────

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'epic_games_username',
            'platform'
        ]


# ─── Optional Initial Profile Form (Not used unless needed) ────

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'last_vbucks_purchase']


# ─── Edit Profile — User Info ─────────────────────────────────

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'epic_games_username',
            'platform'
        ]


# ─── Edit Profile — Avatar ────────────────────

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']