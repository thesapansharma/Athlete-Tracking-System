# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.contrib.auth.models import User
from authentication.models import CustomUser

# Register your models here.
admin.site.register(User, CustomUser)
admin.site.register(CustomUser)