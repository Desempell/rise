from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_user, name="register_user"),
    path("login/", views.login_user, name="login_user"),
    path("user/", views.get_user, name="get_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("delete_user/", views.delete_user, name="delete_user"),
    path("create_expenses/", views.create_expenses, name="create_expenses"),
    path("create_suggestion/", views.create_suggestion, name="create_suggestion"),
    path('create-expense-type/', views.create_expense_type, name='create-expense-type'),
    path('create-suggestion-type/', views.create_suggestion_type, name='create-suggestion-type')
]