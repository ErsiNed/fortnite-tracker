from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from .models import RealMoneyTransaction
from .forms import RealMoneyTransactionForm


class HomePageView(TemplateView):
    template_name = "dashboard.html"


class RealMoneyTransactionListView(LoginRequiredMixin, ListView):
    model = RealMoneyTransaction
    template_name = 'transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return RealMoneyTransaction.objects.filter(user=self.request.user)


class RealMoneyTransactionCreateView(LoginRequiredMixin, CreateView):
    model = RealMoneyTransaction
    form_class = RealMoneyTransactionForm
    template_name = 'transaction_form.html'
    success_url = reverse_lazy('vbucks_tracker:transaction-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RealMoneyTransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = RealMoneyTransaction
    form_class = RealMoneyTransactionForm
    template_name = 'transaction_form.html'
    success_url = reverse_lazy('vbucks_tracker:transaction-list')

    def get_queryset(self):
        return RealMoneyTransaction.objects.filter(user=self.request.user)


class RealMoneyTransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = RealMoneyTransaction
    template_name = 'transaction_confirm_delete.html'
    success_url = reverse_lazy('vbucks_tracker:transaction-list')

    def get_queryset(self):
        return RealMoneyTransaction.objects.filter(user=self.request.user)
