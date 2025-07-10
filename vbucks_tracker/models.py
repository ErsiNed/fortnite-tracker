from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from accounts.models import User


class RealMoneyTransaction(models.Model):
    CATEGORIES = [
        ('VB', 'V-Bucks'),
        ('CREW', 'Fortnite Crew'),
        ('QUEST', 'Quest Pack'),
        ('PACK', 'Skin Pack'),
        ('OTHER', 'Other'),
    ]

    CURRENCIES = [
        ('BGN', 'BGN (Bulgarian Lev)'),
        ('EUR', 'EUR (Euro)'),
        ('USD', 'USD (US Dollar)'),
        ('GBP', 'GBP (British Pound)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='real_money_transactions')
    category = models.CharField(max_length=10, choices=CATEGORIES, default='VB')
    source_name = models.CharField(
        max_length=100,
        help_text="Specify the exact name, e.g. 'Season 7 Battle Pass' or 'Quest Pack 3'"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    vbucks_earned = models.PositiveIntegerField(
        default=0,
        help_text="Amount of V-Bucks received from this transaction"
    )
    date = models.DateField()
    currency = models.CharField(
        max_length=5,
        choices=CURRENCIES,
        default='BGN'
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Real Money Transaction'
        verbose_name_plural = 'Real Money Transactions'
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.get_category_display()} - {self.source_name} - {self.amount} {self.currency}"

    def clean(self):
        if self.date and self.date > timezone.now().date():
            raise ValidationError("Transaction date cannot be in the future")


class VbucksEarning(models.Model):
    EARNING_TYPES = [
        ('BP', 'Battle Pass'),
        ('CREW', 'Fortnite Crew'),
        ('QUEST', 'Quest Pack'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vbucks_earnings')
    type = models.CharField(max_length=10, choices=EARNING_TYPES, default="BP")
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    date = models.DateField()
    earning_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional name for this earning"
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'V-Bucks Earning'
        verbose_name_plural = 'V-Bucks Earnings'
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.get_type_display()}: {self.amount} V-Bucks"

    def clean(self):
        if self.date and self.date > timezone.now().date():
            raise ValidationError("Earning date cannot be in the future")


class VbucksSpending(models.Model):
    CATEGORIES = [
        ('SKIN', 'Skin'),
        ('EMOTE', 'Emote'),
        ('BUNDLE', 'Bundle'),
        ('GIFT', 'Gift'),
        ('BP', 'Battle Pass'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vbucks_spendings')
    item_name = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=CATEGORIES, default='SKIN')
    vbucks_spent = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    date = models.DateField()
    refunded = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']
        verbose_name = 'V-Bucks Spending'
        verbose_name_plural = 'V-Bucks Spendings'
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['refunded']),
        ]

    def __str__(self):
        refund_status = " (Refunded)" if self.refunded else ""
        return f"{self.item_name} - {self.vbucks_spent} V-Bucks{refund_status}"

    def clean(self):
        if self.date and self.date > timezone.now().date():
            raise ValidationError("Spending date cannot be in the future")


class Refund(models.Model):
    REFUND_REASONS = [
        ('DISAPPOINTED', 'Item Disappointed Me'),
        ('ACCIDENTAL', 'Accidental Purchase'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='refunds',
        verbose_name="User"
    )
    original_purchase = models.ForeignKey(
        'VbucksSpending',
        on_delete=models.CASCADE,
        related_name='refund',
        verbose_name="Original Purchase"
    )
    vbucks_returned = models.PositiveIntegerField(
        editable=False,
        verbose_name="V-Bucks Returned",
        help_text="Automatically set to match original purchase amount"
    )
    refund_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Refund Date"
    )
    reason = models.CharField(
        max_length=200,
        choices=REFUND_REASONS,
        blank=True,
        verbose_name="Reason",
        help_text="Select the reason for this refund"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Additional Notes"
    )

    class Meta:
        ordering = ['-refund_date']
        verbose_name = 'Refund'
        verbose_name_plural = 'Refunds'
        indexes = [
            models.Index(fields=['user', 'refund_date']),
            models.Index(fields=['original_purchase']),
        ]

    def __str__(self):
        return f"Refund of {self.vbucks_returned} V-Bucks ({self.get_reason_display()})"

    def clean(self):
        """Validate the refund before saving"""
        if not hasattr(self, 'original_purchase'):
            raise ValidationError("Original purchase must be selected")
        if self.original_purchase.refunded:
            raise ValidationError("This purchase has already been refunded")
        self.vbucks_returned = self.original_purchase.vbucks_spent  # Auto-set amount

    def save(self, *args, **kwargs):
        """Handle purchase status on save"""
        self.full_clean()
        if not self.original_purchase.refunded:
            self.original_purchase.refunded = True
            self.original_purchase.save(update_fields=['refunded'])
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Handle purchase status on delete"""
        purchase = self.original_purchase
        super().delete(*args, **kwargs)
        purchase.refunded = False
        purchase.save(update_fields=['refunded'])


    @property
    def purchase_details(self):
        """Helper property to access purchase info"""
        return {
            'item_name': self.original_purchase.item_name,
            'original_amount': self.original_purchase.vbucks_spent,
            'purchase_date': self.original_purchase.date
        }
