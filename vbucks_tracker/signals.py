from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import VbucksEarning, VbucksSpending, Refund, RealMoneyTransaction


def recalculate_vbucks_balance(user):
    total_earned = (
        VbucksEarning.objects.filter(user=user).aggregate(total=models.Sum('amount'))['total'] or 0
    )
    total_purchased = (
        RealMoneyTransaction.objects.filter(user=user).aggregate(total=models.Sum('vbucks_earned'))['total'] or 0
    )
    total_spent = (
        VbucksSpending.objects.filter(user=user, refunded=False).aggregate(total=models.Sum('vbucks_spent'))['total'] or 0
    )
    total_refunded = (
        Refund.objects.filter(user=user).aggregate(total=models.Sum('vbucks_returned'))['total'] or 0
    )

    user.vbucks_balance = (total_earned + total_purchased + total_refunded) - total_spent
    user.save(update_fields=['vbucks_balance'])


@receiver(post_save, sender=RealMoneyTransaction)
def create_or_update_vbucks_earning(sender, instance, created, **kwargs):
    # Mapping RealMoneyTransaction categories to VbucksEarning types
    category_to_type = {
        'VB': 'PURCHASE',
        'CREW': 'CREW',
        'QUEST': 'QUEST',
        'OTHER': 'OTHER',
    }

    earning_type = category_to_type.get(instance.category)

    if earning_type and instance.vbucks_earned > 0:
        VbucksEarning.objects.update_or_create(
            user=instance.user,
            earning_name=instance.source_name,
            date=instance.date,
            defaults={
                'type': earning_type,
                'amount': instance.vbucks_earned,
            }
        )
    else:
        # For PACK (vbucks_earned=0) or any other with 0, delete existing earning if any
        VbucksEarning.objects.filter(
            user=instance.user,
            earning_name=instance.source_name,
            date=instance.date
        ).delete()


@receiver([post_save, post_delete], sender=VbucksEarning)
@receiver([post_save, post_delete], sender=RealMoneyTransaction)
@receiver([post_save, post_delete], sender=VbucksSpending)
@receiver([post_save, post_delete], sender=Refund)
def update_vbucks_balance(sender, instance, **kwargs):
    recalculate_vbucks_balance(instance.user)