# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from app import admin

class CustomUser(AbstractUser):
    SPORT_CHOICES = [
        ('football', 'Football'),
        ('basketball', 'Basketball'),
        ('badminton', 'Badminton'),
        ('vollyball', 'Vollyball'),
        ('squash', 'Squash'),
        ('fencing', 'Fencing'),
        ('gymnastics', 'Gymnastics'),
        ('cricket', 'Cricket'),
        ('swimming', 'Swimming'),
        ('tennis', 'Tennis')
    ]
    
    sport = models.CharField(
        max_length=30,
        choices=SPORT_CHOICES,
        default='draft'
    )
    is_Coach = models.BooleanField(default=False, blank=True,null=True)

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(upload_to='core/media', blank=True, null=True)
    identification = models.FileField(upload_to='identifications/', blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_phone_number = models.CharField(max_length=15, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_phone_number = models.CharField(max_length=15, blank=True, null=True)


   