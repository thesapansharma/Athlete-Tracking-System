
from datetime import timedelta
from background_task import background
from django.core.mail import send_mail
from django.utils import timezone
from app.CompetitionModel import DietPlan, ExercisePlan
from app.models import CustomUser, WeeklyReflection

@background(schedule=60)  # Runs every minute; adjust as needed
def send_daily_reminders():
    today = timezone.now().date()
    athletes = CustomUser.objects.filter(is_Coach=True)

    for athlete in athletes:
        exercise_plan = ExercisePlan.objects.filter(user=athlete).first()
        if exercise_plan:
            send_mail(
                'Daily Exercise Reminder',
                f'Hi {athlete.username},\n\nRemember to follow your exercise plan:\n{exercise_plan.details}',
                'mailtrap@demomailtrap.com',
                ["sapansharma000ss@gmail.com"],
                fail_silently=False,
            )

        diet_plan = DietPlan.objects.filter(user=athlete).first()
        if diet_plan:
            send_mail(
                'Daily Diet Plan Reminder',
                f'Hi {athlete.username},\n\nHere is your diet plan for today:\n{diet_plan.details}',
                'mailtrap@demomailtrap.com',
                ['sapansharma000ss@gmail.com'],
                fail_silently=False,
            )
@background(schedule=60*60*24*7)  # Runs every week; adjust as needed
def send_weekly_reflection_reminders():
    today = timezone.now().date()
    last_week = today - timedelta(days=7)

    athletes = CustomUser.objects.filter(is_Coach=True)

    for athlete in athletes:
        if not WeeklyReflection.objects.filter(athlete=athlete, date__gte=last_week).exists():
            send_mail(
                'Weekly Reflection Reminder',
                f'Hi {athlete.username},\n\nIt\'s time to fill out your weekly reflection form.',
                'from@example.com',
                [athlete.email],
                fail_silently=False,
            )