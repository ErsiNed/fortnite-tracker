from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_vbucks_summary(self):
        """Get V-Bucks summary through the service layer"""
        from vbucks_tracker.services import VbucksService
        return VbucksService.get_user_summary(self)

    @property
    def vbucks_balance(self):
        """Shortcut property for the balance"""
        return self.get_vbucks_summary()['balance']

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="User Profile"
    )
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/%d/',
        blank=True,
        verbose_name="Profile Picture",
        help_text="Upload a profile picture (square image works best)",
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    epic_games_username = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Epic Games Username"
    )

    PLATFORMS = [
        ('PC', 'PC'),
        ('PS', 'PlayStation'),
        ('XB', 'Xbox'),
        ('NS', 'Nintendo Switch'),
        ('MOBILE', 'Mobile'),
    ]
    platform = models.CharField(
        max_length=10,
        choices=PLATFORMS,
        blank=True,
        verbose_name="Main Platform"
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def clean(self):
        super().clean()
        if self.epic_games_username and not self.epic_games_username.replace('_', '').isalnum():
            raise ValidationError(
                "Epic Games username should contain only letters, numbers and underscores"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile for {self.user.username}"