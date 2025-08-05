from datetime import timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import User
from vbucks_tracker.models import RealMoneyTransaction, VbucksSpending, Refund


class RealMoneyTransactionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='transaction_test', password='test123')

    def test_transaction_creation(self):
        txn = RealMoneyTransaction.objects.create(
            user=self.user,
            category='VB',
            source_name='Test Purchase',
            amount=10.99,
            vbucks_earned=1000,
            currency='USD',
            date=timezone.now().date()
        )
        self.assertEqual(txn.get_category_display(), 'V-Bucks')

    def test_future_date_validation(self):
        future_date = timezone.now().date() + timedelta(days=1)
        txn = RealMoneyTransaction(
            user=self.user,
            category='VB',
            source_name='Invalid Date',
            amount=10,
            vbucks_earned=1000,
            date=future_date
        )
        with self.assertRaises(ValidationError):
            txn.full_clean()


class VbucksSpendingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='spending_test', password='test123')
        self.spending = VbucksSpending.objects.create(
            user=self.user,
            item_name='Rainbow Smasher',
            category='SKIN',
            vbucks_spent=1500,
            date=timezone.now().date()
        )

    def test_refund_toggle(self):
        self.spending.refunded = True
        self.spending.save()
        self.assertTrue(self.spending.refunded)


class RefundIntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='refund_test', password='test123')
        self.purchase = VbucksSpending.objects.create(
            user=self.user,
            item_name='Minty Axe',
            vbucks_spent=2000,
            date=timezone.now().date()
        )

    def test_refund_workflow(self):
        refund = Refund.objects.create(
            user=self.user,
            original_purchase=self.purchase,
            reason='DISAPPOINTED')

        self.purchase.refresh_from_db()
        self.assertTrue(self.purchase.refunded)

        refund.delete()
        self.purchase.refresh_from_db()
        self.assertFalse(self.purchase.refunded)