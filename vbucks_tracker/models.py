from django.db import models
from django.utils import timezone
from accounts.models import User


class RealMoneyTransaction(models.Model):
    CATEGORIES = [
        ('VB', 'V-Bucks'),
        ('CREW', 'Fortnite Crew'),
        ('QUEST', 'Quest Pack'),
        ('PACK', 'Skin Pack'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORIES, default='VB')
    source_name = models.CharField(
        max_length=100,
        help_text="Specify the exact name, e.g. 'Season 7 Battle Pass' or 'Quest Pack 3'"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    vbucks_earned = models.PositiveIntegerField(default=0)
    date = models.DateField()
    currency = models.CharField(max_length=5, default='BGN')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_category_display()} - {self.source_name} - {self.amount} {self.currency}"


class VbucksEarning(models.Model):
    EARNING_TYPES = [
        ('PURCHASE', 'V-Bucks Purchase'),
        ('BP', 'Battle Pass'),
        ('CREW', 'Fortnite Crew'),
        ('QUEST', 'Quest Pack'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=EARNING_TYPES)
    amount = models.PositiveIntegerField()
    date = models.DateField()
    earning_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.amount} V-Bucks"


class VbucksSpending(models.Model):
    CATEGORIES = [
        ('SKIN', 'Skin'),
        ('EMOTE', 'Emote'),
        ('BUNDLE', 'Bundle'),
        ('GIFT', 'Gift'),
        ('BP', 'Battle Pass'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=CATEGORIES)
    vbucks_spent = models.PositiveIntegerField()
    date = models.DateField()
    refunded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item_name} ({self.vbucks_spent} V-Bucks)"


class Refund(models.Model):
    REFUND_REASONS = [
        ('ACCIDENTAL', 'Accidental Purchase'),
        ('DISAPPOINTED', 'Item Disappointed Me'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_purchase = models.ForeignKey(VbucksSpending, on_delete=models.CASCADE)
    vbucks_returned = models.PositiveIntegerField(blank=True, null=True)
    refund_date = models.DateTimeField(default=timezone.now)
    reason = models.CharField(max_length=200, blank=True, choices=REFUND_REASONS)

    def __str__(self):
        return f"Refund of {self.vbucks_returned} V-Bucks"