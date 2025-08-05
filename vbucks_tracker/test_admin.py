from django.test import TestCase, Client
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from accounts.models import User
from vbucks_tracker.models import VbucksEarning


class AdminPermissionTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass')

        self.staff = User.objects.create_user(
            username='staff',
            password='staffpass',
            is_staff=True)

        view_perm = Permission.objects.get(codename='view_vbucksearning')
        change_perm = Permission.objects.get(codename='change_vbucksearning')

        staff_group = Group.objects.create(name='Staff')
        staff_group.permissions.add(view_perm, change_perm)
        self.staff.groups.add(staff_group)

        # Create test data
        self.earning = VbucksEarning.objects.create(
            user=self.admin,
            type='BP',
            amount=1500,
            date='2023-01-01'
        )

    def test_staff_can_view_earnings(self):
        self.client.login(username='staff', password='staffpass')
        response = self.client.get(reverse('admin:vbucks_tracker_vbucksearning_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Battle Pass')

    def test_staff_cannot_delete(self):
        self.client.login(username='staff', password='staffpass')
        url = reverse('admin:vbucks_tracker_vbucksearning_delete', args=[self.earning.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)