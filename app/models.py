# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models

from authentication.models import CustomUser

class WeeklyReflection(models.Model):
    # Field to store the date of the reflection
    date = models.DateField()
    athlete_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reflections')

    # Field to store the title of the reflection
    title = models.CharField(max_length=200)

    # Text fields for reflections
    what_went_well = models.TextField()
    even_better_if = models.TextField()

    # Choices for diet plan and exercise routine helpfulness
    DIET_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    exercise_routine_helpful = models.CharField(
        max_length=3,
        choices=DIET_CHOICES,
        default='No'
    )

    diet_plan_helpful = models.CharField(
        max_length=3,
        choices=DIET_CHOICES,
        default='No'
    )

    # Rating fields
    ENDURANCE_CHOICES = [(i, i) for i in range(1, 6)]
    FLEXIBILITY_CHOICES = [(i, i) for i in range(1, 6)]
    PROGRESS_CHOICES = [(i, i) for i in range(1, 6)]
    MOTIVATION_CHOICES = [(i, i) for i in range(1, 6)]

    endurance = models.PositiveSmallIntegerField(choices=ENDURANCE_CHOICES, default=1)
    flexibility = models.PositiveSmallIntegerField(choices=FLEXIBILITY_CHOICES, default=1)
    progress = models.PositiveSmallIntegerField(choices=PROGRESS_CHOICES, default=1)
    motivation = models.PositiveSmallIntegerField(choices=MOTIVATION_CHOICES, default=1)

    def __str__(self):
        return f"Reflection on {self.date} - {self.athlete.username} - {self.title}"
