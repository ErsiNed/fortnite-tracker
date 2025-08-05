from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User, UserProfile
from vbucks_tracker.models import RealMoneyTransaction, VbucksEarning, VbucksSpending, Refund


class Command(BaseCommand):
    help = 'Sets up the Staff group with specific permissions for user and vbucks models.'

    def handle(self, *args, **options):
        staff_group, created = Group.objects.get_or_create(name='Staff')

        # Permissions for User and UserProfile
        user_models = [User, UserProfile]
        for model in user_models:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(
                content_type=ct,
                codename__in=[
                    f'view_{model._meta.model_name}',
                    f'change_{model._meta.model_name}'
                ]
            )
            staff_group.permissions.add(*perms)

        # Permissions for Vbucks-related models
        vbucks_models = [RealMoneyTransaction, VbucksEarning, VbucksSpending, Refund]
        for model in vbucks_models:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(
                content_type=ct,
                codename__in=[
                    f'view_{model._meta.model_name}',
                    f'change_{model._meta.model_name}'
                ]
            )
            staff_group.permissions.add(*perms)

        self.stdout.write(self.style.SUCCESS('Staff group and permissions set up successfully.'))