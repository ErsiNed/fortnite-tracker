from django import forms
from .models import RealMoneyTransaction, VbucksEarning, VbucksSpending, Refund
from django.core.exceptions import ValidationError
from django.utils import timezone


class RealMoneyTransactionForm(forms.ModelForm):
    class Meta:
        model = RealMoneyTransaction
        fields = ['category', 'source_name', 'amount', 'vbucks_earned', 'date', 'currency', 'notes']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'max': timezone.now().date().isoformat()  # Prevent future dates
                },
                format='%Y-%m-%d'
            ),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'vbucks_earned': 'Enter the amount of V-Bucks received from this transaction',
            'source_name': 'e.g. "Season 7 Battle Pass" or "Quest Pack 3"'
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        return amount


class VbucksEarningForm(forms.ModelForm):
    class Meta:
        model = VbucksEarning
        fields = ['type', 'amount', 'date', 'earning_name']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'max': timezone.now().date().isoformat()
                }
            ),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError("V-Bucks amount must be positive")
        return amount


class VbucksSpendingForm(forms.ModelForm):
    class Meta:
        model = VbucksSpending
        fields = ['item_name', 'category', 'vbucks_spent', 'date',]
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'max': timezone.now().date().isoformat()
                }
            ),
            'item_name': forms.TextInput(attrs={'placeholder': 'e.g. "Skull Trooper Skin"'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show non-refunded purchases for refund selection
        if 'initial' in kwargs and 'original_purchase' in kwargs['initial']:
            self.fields['refunded'].disabled = True

    def clean_vbucks_spent(self):
        vbucks = self.cleaned_data['vbucks_spent']
        if vbucks <= 0:
            raise ValidationError("V-Bucks spent must be positive")
        return vbucks


class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['original_purchase', 'reason']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['original_purchase'].queryset = (
                VbucksSpending.objects.filter(user=user, refunded=False)
            )

from django import forms

class GiftedSpendingFilterForm(forms.Form):
    category = forms.ChoiceField(
        choices=[
            ('', 'All Categories'),
            ('GIFT', 'Gifted Only'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm',
            'onchange': 'this.form.submit()'
        })
    )