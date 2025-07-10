from django.urls import path, include
from . import views

app_name = 'vbucks_tracker'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),

    # Transactions
    path('transactions/', include([
        path('', views.RealMoneyTransactionListView.as_view(), name='transaction-list'),
        path('add/', views.RealMoneyTransactionCreateView.as_view(), name='transaction-create'),
        path('<int:pk>/edit/', views.RealMoneyTransactionUpdateView.as_view(), name='transaction-update'),
        path('<int:pk>/delete/', views.RealMoneyTransactionDeleteView.as_view(), name='transaction-delete'),
    ])),

    # V-Bucks Earnings
    path('vbucks-earnings/', include([
        path('', views.VbucksEarningListView.as_view(), name='vbucksearning-list'),
        path('add/', views.VbucksEarningCreateView.as_view(), name='vbucksearning-create'),
        path('<int:pk>/edit/', views.VbucksEarningUpdateView.as_view(), name='vbucksearning-update'),
        path('<int:pk>/delete/', views.VbucksEarningDeleteView.as_view(), name='vbucksearning-delete'),
    ])),

    # V-Bucks Spendings
    path('vbucks-spendings/', include([
        path('', views.VbucksSpendingListView.as_view(), name='vbucks-spending-list'),
        path('add/', views.VbucksSpendingCreateView.as_view(), name='vbucks-spending-create'),
        path('<int:pk>/edit/', views.VbucksSpendingUpdateView.as_view(), name='vbucks-spending-update'),
        path('<int:pk>/delete/', views.VbucksSpendingDeleteView.as_view(), name='vbucks-spending-delete'),
    ])),

    # Refunds
    path('refunds/', include([
        path('', views.RefundListView.as_view(), name='refund-list'),
        path('add/', views.RefundCreateView.as_view(), name='refund-create'),
        path('<int:pk>/delete/', views.RefundDeleteView.as_view(), name='refund-delete'),
    ])),
]
