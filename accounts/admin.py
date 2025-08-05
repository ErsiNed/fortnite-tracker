from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fields = ('avatar_preview', 'epic_games_username', 'platform')
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        return format_html(
            '<img src="{}" style="max-height:100px;max-width:100px;"/>',
            obj.avatar.url
        ) if obj.avatar else "No avatar"

    avatar_preview.short_description = 'Preview'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'vbucks_balance', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'profile__epic_games_username')
    ordering = ('-date_joined',)

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            return [
                (None, {'fields': ('username',)}),
                ('Info', {'fields': ('first_name', 'last_name', 'email')}),
                ('Status', {'fields': ('is_active',)}),
            ]
        return super().get_fieldsets(request, obj)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'epic_username')
    list_filter = ('platform',)
    search_fields = ('user__username', 'epic_games_username')

    @staticmethod
    def epic_username(obj):
        return obj.epic_games_username or "-"

    epic_username.short_description = 'Epic ID'


def setup_staff_group():
    """Configure Staff group with limited permissions"""
    staff, _ = Group.objects.get_or_create(name='Staff')
    for model in [User, UserProfile]:
        ct = ContentType.objects.get_for_model(model)
        staff.permissions.add(*Permission.objects.filter(
            content_type=ct,
            codename__in=['view_user', 'change_user', 'view_userprofile', 'change_userprofile']
        ))


admin.site.register(User, CustomUserAdmin)
setup_staff_group()