from django.db.models import Sum
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from .models import RealMoneyTransaction, VbucksEarning, VbucksSpending, Refund
from .forms import RealMoneyTransactionForm, VbucksEarningForm, VbucksSpendingForm, RefundForm
from .services import VbucksService

# Constants for reusable templates
BASE_FORM_TEMPLATE = 'base_form.html'
BASE_DELETE_TEMPLATE = 'base_delete.html'


class HomePageView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            summary = VbucksService.get_user_summary(self.request.user)
            context.update({
                'total_spent': summary['total_spent'],
                'total_earned': summary['total_earned'],
                'total_real_money': RealMoneyTransaction.objects.filter(
                    user=self.request.user
                ).aggregate(Sum('amount'))['amount__sum'] or 0,
                'total_refunds': summary['total_refunded'],
                'vbucks_balance': summary['balance']
            })
        return context


# Base View Classes
class BaseCreateView(LoginRequiredMixin, CreateView):
    template_name = BASE_FORM_TEMPLATE

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.model._meta.verbose_name
        context.update({
            'form_title': f'Add {model_name}',
            'submit_text': f'Create {model_name}',
            'cancel_url': self.success_url,
        })
        return context


class BaseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = BASE_FORM_TEMPLATE

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.model._meta.verbose_name
        context.update({
            'form_title': f'Edit {model_name}',
            'submit_text': f'Update {model_name}',
            'cancel_url': self.success_url,
        })
        return context


class BaseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = BASE_DELETE_TEMPLATE

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.model._meta.verbose_name
        context.update({
            'title': f'Delete {model_name}',
            'message': f'Are you sure you want to delete this {model_name.lower()}?',
            'cancel_url': self.success_url,
            'confirm_button': f'Delete {model_name}',
        })
        return context


class BaseListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)

        # Apply ordering only if specified by child class
        if hasattr(self, 'ordering') and self.ordering:
            return queryset.order_by(*self.ordering)
        return queryset


# RealMoneyTransaction Views
class RealMoneyTransactionListView(BaseListView):
    model = RealMoneyTransaction
    template_name = 'real_money_transaction_list.html'
    context_object_name = 'transactions'


class RealMoneyTransactionCreateView(BaseCreateView):
    model = RealMoneyTransaction
    form_class = RealMoneyTransactionForm
    success_url = reverse_lazy('vbucks_tracker:transaction-list')


class RealMoneyTransactionUpdateView(BaseUpdateView):
    model = RealMoneyTransaction
    form_class = RealMoneyTransactionForm
    success_url = reverse_lazy('vbucks_tracker:transaction-list')


class RealMoneyTransactionDeleteView(BaseDeleteView):
    model = RealMoneyTransaction
    success_url = reverse_lazy('vbucks_tracker:transaction-list')


# VbucksEarning Views
class VbucksEarningListView(BaseListView):
    model = VbucksEarning
    template_name = 'vbucks_earning_list.html'
    context_object_name = 'earnings'


class VbucksEarningCreateView(BaseCreateView):
    model = VbucksEarning
    form_class = VbucksEarningForm
    success_url = reverse_lazy('vbucks_tracker:vbucksearning-list')


class VbucksEarningUpdateView(BaseUpdateView):
    model = VbucksEarning
    form_class = VbucksEarningForm
    success_url = reverse_lazy('vbucks_tracker:vbucksearning-list')


class VbucksEarningDeleteView(BaseDeleteView):
    model = VbucksEarning
    success_url = reverse_lazy('vbucks_tracker:vbucksearning-list')


# VbucksSpending Views
class VbucksSpendingListView(BaseListView):
    model = VbucksSpending
    template_name = 'vbucks_spending_list.html'
    context_object_name = 'spendings'


class VbucksSpendingCreateView(BaseCreateView):
    model = VbucksSpending
    form_class = VbucksSpendingForm
    success_url = reverse_lazy('vbucks_tracker:vbucks-spending-list')


class VbucksSpendingUpdateView(BaseUpdateView):
    model = VbucksSpending
    form_class = VbucksSpendingForm
    success_url = reverse_lazy('vbucks_tracker:vbucks-spending-list')


class VbucksSpendingDeleteView(BaseDeleteView):
    model = VbucksSpending
    success_url = reverse_lazy('vbucks_tracker:vbucks-spending-list')


# Refund Views
class RefundListView(BaseListView):
    model = Refund
    template_name = 'refund_list.html'
    context_object_name = 'refunds'
    ordering = ['-refund_date']


class RefundCreateView(BaseCreateView):
    model = Refund
    form_class = RefundForm
    success_url = reverse_lazy('vbucks_tracker:refund-list')

    def get_form_kwargs(self):
        """Pass the user to the form for purchase filtering"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Auto-set user and calculate vbucks_returned"""
        form.instance.user = self.request.user
        form.instance.vbucks_returned = form.cleaned_data['original_purchase'].vbucks_spent
        return super().form_valid(form)


class RefundDeleteView(BaseDeleteView):
    model = Refund
    success_url = reverse_lazy('vbucks_tracker:refund-list')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
