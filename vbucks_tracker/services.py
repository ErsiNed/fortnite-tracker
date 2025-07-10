from django.db.models import Sum
from .models import RealMoneyTransaction, VbucksEarning, VbucksSpending, Refund


class VbucksService:
    @staticmethod
    def get_user_balance(user):
        """Calculate the user's current V-Bucks balance"""
        purchased = RealMoneyTransaction.objects.filter(user=user).aggregate(
            total=Sum('vbucks_earned')
        )['total'] or 0

        earned = VbucksEarning.objects.filter(user=user).aggregate(
            total=Sum('amount')
        )['total'] or 0

        spent = VbucksSpending.objects.filter(user=user, refunded=False).aggregate(
            total=Sum('vbucks_spent')
        )['total'] or 0

        return purchased + earned - spent

    @staticmethod
    def get_user_summary(user):
        """Get a complete financial summary for the user"""
        return {
            'total_purchased': RealMoneyTransaction.objects.filter(user=user).aggregate(
                total=Sum('vbucks_earned')
            )['total'] or 0,
            'total_earned': VbucksEarning.objects.filter(user=user).aggregate(
                total=Sum('amount')
            )['total'] or 0,
            'total_spent': VbucksSpending.objects.filter(user=user, refunded=False).aggregate(
                total=Sum('vbucks_spent')
            )['total'] or 0,
            'total_refunded': Refund.objects.filter(user=user).aggregate(
                total=Sum('vbucks_returned')
            )['total'] or 0,
            'balance': VbucksService.get_user_balance(user)
        }