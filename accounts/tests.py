from unittest.mock import patch
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User, UserProfile

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)

    def test_vbucks_balance_property(self):
        with patch('vbucks_tracker.services.VbucksService') as mock_service:
            mock_service.get_user_summary.return_value = {'balance': 5000}
            self.assertEqual(self.user.vbucks_balance, 5000)
            mock_service.get_user_summary.assert_called_once_with(self.user)

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profiletest', password='test123')
        self.profile = UserProfile.objects.create(
            user=self.user,
            epic_games_username='test_epic123',
            platform='PC'
        )

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "Profile for profiletest")

    def test_epic_username_validation(self):
        self.profile.epic_games_username = 'invalid!name'
        with self.assertRaises(ValidationError):
            self.profile.full_clean()

    def test_avatar_upload(self):
        test_image = SimpleUploadedFile(
            name='test.png',
            content=b'smallfakeimagedata',
            content_type='image/png'
        )
        self.profile.avatar = test_image
        self.profile.save()
        self.assertIn('test', self.profile.avatar.name)