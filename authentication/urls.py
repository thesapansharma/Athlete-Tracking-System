# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from . import views
from .views import login_view, logout_user, register_user, update_profile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", logout_user, name="logout"),
    path("profile/", update_profile, name="profile"),
    path('request-password-reset/', views.request_password_reset, name='request_password_reset'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('set-new-password/', views.set_new_password, name='set_new_password')
]
