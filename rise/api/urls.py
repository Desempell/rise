from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(authentication_form=views.UserLoginForm), name="login_user"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout_user"),
    path("register/", views.register_user, name="register_user"),
    path("profile/", views.user_profile, name="profile"),
]