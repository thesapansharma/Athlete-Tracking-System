from django.db import models
from django.contrib.auth.models import User
from authentication.models import CustomUser
from django.utils import timezone

class Competition(models.Model):
    sport = models.CharField(max_length=30, choices=CustomUser.SPORT_CHOICES)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.get_sport_display()}"

class Result(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    athlete = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    result = models.CharField(max_length=100)  # e.g., score, time

    def __str__(self):
        return f"{self.athlete.username} - {self.result}"

class DietPlan(models.Model):
    coach = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_diets')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='diet_plans')
    assigned_date = models.DateTimeField(default=timezone.now)
    breakfast = models.TextField(blank=True, null=True)
    lunch = models.TextField(blank=True, null=True)
    snack = models.TextField(blank=True, null=True)
    dinner = models.TextField(blank=True, null=True)
    pdf_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-assigned_date']

    def __str__(self):
        return f'Diet Plan for {self.user.username} by {self.coach.username} on {self.assigned_date}'
    

class ExercisePlan(models.Model):
    coach = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_exercise')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='exercise_plans')
    assigned_date = models.DateTimeField(auto_now_add=True)
    stretching = models.TextField(blank=True, null=True)
    endurance = models.TextField(blank=True, null=True)
    weights = models.TextField(blank=True, null=True)
    sports_specific = models.TextField(blank=True, null=True)
    pdf_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-assigned_date']

    def __str__(self):
        return f'Exercise Plan for {self.user.username} by {self.coach.username} on {self.assigned_date}'
    

class TaskChecklist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)