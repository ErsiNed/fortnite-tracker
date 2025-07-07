from django.urls import path
from . import views

app_name = 'vbucks_tracker'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('transactions/', views.RealMoneyTransactionListView.as_view(), name='transaction-list'),
    path('transactions/add/', views.RealMoneyTransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/edit/', views.RealMoneyTransactionUpdateView.as_view(), name='transaction-update'),
    path('transactions/<int:pk>/delete/', views.RealMoneyTransactionDeleteView.as_view(), name='transaction-delete'),
]