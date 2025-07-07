from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError


class User(AbstractUser):
    epic_games_username = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Epic Games Username"
    )
    vbucks_balance = models.PositiveIntegerField(
        default=0,
        verbose_name="V-Bucks Balance"
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
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def total_money_spent(self):
        """Total real money spent (BGN) from all transactions"""
        from vbucks_tracker.models import RealMoneyTransaction
        return RealMoneyTransaction.objects.filter(user=self).aggregate(
            total=Sum('amount')
        )['total'] or 0

    @property
    def total_vbucks_earned(self):
        """Total V-Bucks earned from all sources"""
        from vbucks_tracker.models import VbucksEarning
        return VbucksEarning.objects.filter(user=self).aggregate(
            total=Sum('amount')
        )['total'] or 0

    @property
    def total_vbucks_spent(self):
        """Total V-Bucks spent (excluding refunded items)"""
        from vbucks_tracker.models import VbucksSpending
        return VbucksSpending.objects.filter(
            user=self,
            refunded=False
        ).aggregate(total=Sum('vbucks_spent'))['total'] or 0

    @property
    def available_vbucks(self):
        """Current usable V-Bucks (automatically calculated)"""
        return self.total_vbucks_earned - self.total_vbucks_spent

    def clean(self):
        """Validation for platform-specific rules"""
        if self.platform == 'MOBILE' and not self.epic_games_username:
            raise ValidationError("Mobile players must provide an Epic Games username")

    def save(self, *args, **kwargs):
        if not self.pk:
            # Save without computing balance on initial save
            super().save(*args, **kwargs)
            return

        self.full_clean()
        self.vbucks_balance = self.available_vbucks
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.epic_games_username or 'No Epic ID'})"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="User Profile"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        verbose_name="Profile Picture"
    )
    last_vbucks_purchase = models.DateField(
        null=True,
        blank=True,
        verbose_name="Last V-Bucks Purchase"
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def save(self, *args, **kwargs):
        """Only perform validation. Balance is updated via signals."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile for {self.user.username}"
