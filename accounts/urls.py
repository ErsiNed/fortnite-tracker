from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/',
         auth_views.LoginView.as_view(
             template_name='login.html',
             redirect_authenticated_user=True
         ),
         name='login'),

    path('logout/',
         auth_views.LogoutView.as_view(
             next_page='vbucks_tracker:home'
         ),
         name='logout'),

    # Registration
    path('register/', views.register_view, name='register'),

    # Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/delete/', views.delete_profile_view, name='delete_profile'),
]