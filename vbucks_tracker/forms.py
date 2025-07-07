from django import forms
from .models import RealMoneyTransaction, VbucksEarning, VbucksSpending, Refund


class RealMoneyTransactionForm(forms.ModelForm):
    class Meta:
        model = RealMoneyTransaction
        fields = ['category', 'source_name', 'amount', 'vbucks_earned', 'date', 'currency', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class VbucksEarningForm(forms.ModelForm):
    class Meta:
        model = VbucksEarning
        fields = ['type', 'amount', 'date', 'earning_name']


class VbucksSpendingForm(forms.ModelForm):
    class Meta:
        model = VbucksSpending
        fields = ['item_name', 'category', 'vbucks_spent', 'date', 'refunded']


class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['original_purchase', 'vbucks_returned', 'reason']