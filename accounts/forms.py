from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import validate_image_file_extension

from .models import UserProfile

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        validators=[validate_image_file_extension],
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['avatar', 'epic_games_username', 'platform']
        widgets = {
            'epic_games_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Epic Games username'
            }),
            'platform': forms.Select(attrs={'class': 'form-select'})
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class EditUserProfileForm(UserProfileForm):
    def clean_epic_games_username(self):
        username = self.cleaned_data.get('epic_games_username')
        if username and not username.replace('_', '').isalnum():
            raise forms.ValidationError(
                "Username should contain only letters, numbers and underscores"
            )
        return username