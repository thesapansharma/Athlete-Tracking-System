# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from collections import defaultdict
from datetime import timedelta
from io import BytesIO
import random
from django.utils import timezone
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from app.models import WeeklyReflection
from authentication.models import CustomUser
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.core.mail import send_mail
from app.CompetitionModel import Competition, Conversation, DietPlan, ExercisePlan, Result, TaskChecklist
from app.form import DietPlanForm, EventForm, ExercisePlanForm, MessageForm, ResultForm, TaskChecklistForm, WeeklyReflectionForm
from django.core.exceptions import PermissionDenied

# @login_required(login_url="/login/")
def index(request):
    return render(request, 'pages/home.html',)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))

    except:

        template = loader.get_template( 'pages/error-404.html' )
        return HttpResponse(template.render(context, request))
@login_required(login_url="/login/")
def weekly_reflection(request):
    if request.method == 'POST':
        form = WeeklyReflectionForm(request.POST)
        print(type(form)) 
        if form.is_valid():
            event = form.save(commit=False)
            event.athlete_id = request.user
            form.save()
            form = WeeklyReflectionForm()
            return render(request, 'pages/weekly_reflection.html', {'form': form})
    else:
        form = WeeklyReflectionForm()

    return render(request, 'pages/weekly_reflection.html', {'form': form})

@login_required(login_url="/login/")
def old_competitions(request):
    profile = request.user
    sport = profile.sport
    if request.user.is_Coach:
        competitions = Competition.objects.filter(sport=sport, date__lt=timezone.now()).order_by('-date')
    elif request.user.is_superuser:
        competitions = Competition.objects.filter( date__lt=timezone.now()).order_by('-date')

    else:
        # For Regular Users: Show only their own diet plans
        competitions = Competition.objects.filter(sport=sport, date__lt=timezone.now()).order_by('-date')
    
    return render(request, 'pages/old_competitions.html', {'competitions': competitions, 'sport': sport})
@login_required(login_url="/login/")
def upcoming_competitions(request):
    profile = request.user
    sport = profile.sport
    if request.user.is_Coach:
        competitions = Competition.objects.filter(sport=sport, date__gte=timezone.now()).order_by('-date')
    elif request.user.is_superuser:
        competitions = Competition.objects.filter( date__gte=timezone.now()).order_by('-date')

    else:
        competitions = Competition.objects.filter(sport=sport, date__gte=timezone.now()).order_by('-date')
    return render(request, 'pages/upcoming_competitions.html', {'competitions': competitions, 'sport': sport})

@login_required(login_url="/login/")
def results(request, competition_id):
    profile = CustomUser.objects.get(user=request.user)
    sport = profile.sport
    competition = get_object_or_404(Competition, id=competition_id, sport=sport)
    results = Result.objects.filter(competition=competition)
    return render(request, 'sports/results.html', {'results': results, 'competition': competition})



@login_required
def manage_events(request):
    profile = request.user
    sport = profile.sport
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.sport = sport
            event.save()
            return redirect('manage_events')
    else:
        form = EventForm()
    if request.user.is_Coach:
      events = Competition.objects.filter(sport=sport)
    elif request.user.is_superuser:
        events = Competition.objects.filter()
    else:
        events = Competition.objects.filter(sport=sport, created_by=request.user)

    return render(request, 'pages/manage_events.html', {'events': events, 'form': form,'current_url_name': request.resolver_match.url_name})


@login_required
def delete_event(request, event_id):
    profile = request.user
    sport = profile.sport
    event = get_object_or_404(Competition, id=event_id, created_by=request.user, sport=sport)
    if request.method == 'POST':
        event.delete()
        return redirect('manage_events')
    return render(request, 'pages/confirm_delete.html', {'event': event})




@login_required
def update_event(request, event_id):
    profile = request.user
    sport = profile.sport
    event = get_object_or_404(Competition, id=event_id, created_by=request.user, sport=sport)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('manage_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'pages/manage_event_form.html', {'form': form, 'event': event})

@login_required(login_url="/login/")
def create_result(request):
    if request.user.is_Coach or request.user.is_staff:
        
        if request.method == 'POST':
            form = ResultForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('result_list')
        else:
            form = ResultForm()
        return render(request, 'pages/create_result.html', {'form': form})
    else:
        # User is not a coach or admin, raise a permission error
        raise PermissionDenied("You do not have permission to access this page.")

@login_required(login_url="/login/")
def result_list(request):
    results = Result.objects.all()
    return render(request, 'pages/result_list.html', {'results': results})
@login_required(login_url="/login/")
def competition_results(request, event_id):
    # Retrieve the competition by primary key
    competition = get_object_or_404(Competition, id=event_id)
    
    # Retrieve all results for the competition
    results = Result.objects.filter(competition=competition)
    
    return render(request, 'pages/result_list.html', {
        'results': results,
        'current_url_name': "result_see",
        'user':request.user
    })

@login_required(login_url="/login/")
def athlete_progress_report(request,athlete_id):
    reflections = WeeklyReflection.objects.filter(athlete_id=athlete_id).order_by('date')

    dates = []
    endurance_ratings = []
    flexibility_ratings = []
    progress_ratings = []
    motivation_ratings = []
    diet_plan_responses = []
    exercise_routine_responses = []

    for reflection in reflections:
        date_str = reflection.date.strftime('%Y-%m-%d')
        dates.append(date_str)
        endurance_ratings.append(reflection.endurance)
        flexibility_ratings.append(reflection.flexibility)
        progress_ratings.append(reflection.progress)
        motivation_ratings.append(reflection.motivation)

        diet_plan_responses.append(reflection.diet_plan_helpful)
        exercise_routine_responses.append(reflection.exercise_routine_helpful)

    diet_plan_numeric_responses = [1 if response == "Yes" else 0 for response in diet_plan_responses]
    exercise_routine_numeric_responses = [1 if response == "Yes" else 0 for response in exercise_routine_responses]
    user_name = request.user.username  
    context = {
        'dates': dates,
        'endurance_ratings': endurance_ratings,
        'flexibility_ratings': flexibility_ratings,
        'progress_ratings': progress_ratings,
        'motivation_ratings': motivation_ratings,
        'diet_plan_responses': diet_plan_responses,
        'exercise_routine_responses': exercise_routine_responses,
        'diet_plan_numeric_responses': diet_plan_numeric_responses,
        'exercise_routine_numeric_responses': exercise_routine_numeric_responses,
        'user_name': user_name
    }
    return render(request, 'pages/chart.html', context)

@login_required(login_url="/login/")
def diet_dashboard(request):
    if request.user.is_Coach:
        # For Coaches and Superusers: Show all diet plans
        diet_plans = DietPlan.objects.filter(coach=request.user).order_by('-created_at')
    elif request.user.is_superuser:
        diet_plans = DietPlan.objects.all().order_by('-created_at')

    else:
        # For Regular Users: Show only their own diet plans
        diet_plans = DietPlan.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'pages/diet_dashboard.html', {'diet_plans': diet_plans})


@login_required(login_url="/login/")
def download_diet_pdf(request, diet_plan_id):
    # Fetch the DietPlan object for the current user
    if request.user.is_Coach:
        # For Coaches and Superusers: Show all diet plans
        diet_plan = get_object_or_404(DietPlan, pk=diet_plan_id, coach=request.user)
    else:
        # For Regular Users: Show only their own diet plans
        diet_plan = get_object_or_404(DietPlan, pk=diet_plan_id, user=request.user)
    
    # Create an HTTP response with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Diet_Plan_{diet_plan.assigned_date.strftime("%Y-%m-%d")}.pdf"'
    
    # Create a PDF using reportlab
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Add Logo at the top of the page
    logo_url = "./core/static/assets/img/brand/logob.png"
    logo_width = 50
    logo_height = 50
    p.drawImage(logo_url, 50, height - logo_height - 10, width=logo_width, height=logo_height)
    
    # Set up fonts and font sizes
    p.setFont("Helvetica-Bold", 14)
    
    # Title Section
    p.drawString(150, height - 80, f"Diet Plan for {diet_plan.user.username}")
    p.setFont("Helvetica", 10)
    p.drawString(150, height - 95, f"Assigned by {diet_plan.coach.username}")
    p.drawString(150, height - 110, f"Assigned on {diet_plan.assigned_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Draw a line to separate the title from the content
    p.setStrokeColor(colors.black)
    p.setLineWidth(1)
    p.line(50, height - 120, width - 50, height - 120)
    
    # Add content sections with improved layout
    p.setFont("Helvetica-Bold", 12)
    y_position = height - 150  # Start position for content

    sections = [
        ("Breakfast", diet_plan.breakfast),
        ("Lunch", diet_plan.lunch),
        ("Snack", diet_plan.snack),
        ("Dinner", diet_plan.dinner),
    ]
    
    for section_title, content in sections:
        p.drawString(100, y_position, section_title + ":")
        text = p.beginText(100, y_position - 15)
        text.setFont("Helvetica", 10)
        text.setTextOrigin(100, y_position - 15)
        text.textLines(content if content else 'Not provided')
        p.drawText(text)
        
        y_position -= 50  # Adjust the y_position for the next section
    
    # Add extra content (AI-generated or additional dietary tips)
    y_position -= 20  # Add space before extra content
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_position, "Nutrition Tips:")
    y_position -= 15
    p.setFont("Helvetica", 10)
    p.drawString(100, y_position, "1. Stay hydrated throughout the day for optimal metabolism.")
    y_position -= 15
    p.drawString(100, y_position, "2. Incorporate a variety of vegetables into your meals for better nutrition.")
    y_position -= 15
    p.drawString(100, y_position, "3. Avoid processed foods and focus on whole, nutrient-dense options.")
    
    # Add footer with page number
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(100, 30, f"Page 1 - Diet Plan for {diet_plan.user.username}")
    
    p.showPage()
    p.save()

    return response



@login_required(login_url="/login/")
def add_diet_plan(request):
    if not request.user.is_Coach:
        return redirect('diet_dashboard')

    if request.method == 'POST':
        form = DietPlanForm(request.POST,current_user=request.user)
        if form.is_valid():
            diet_plan = form.save(commit=False)
            diet_plan.coach = request.user
            diet_plan.save()
            return redirect('diet_dashboard')
    else:
        form = DietPlanForm(current_user=request.user)

    return render(request, 'pages/add_diet_plan.html', {'form': form})

    
    pdf = buffer.getvalue()
    buffer.close()
    return pdf



@login_required(login_url="/login/")
def exercise_dashboard(request):
    # Order diet plans by created_at in descending order
    if request.user.is_Coach:
        # For Coaches and Superusers: Show all diet plans
        exercise_plans = ExercisePlan.objects.filter(coach=request.user).order_by('-created_at')
    elif request.user.is_superuser:
        exercise_plans = ExercisePlan.objects.all().order_by('-created_at')

    else:
        # For Regular Users: Show only their own diet plans
        exercise_plans = ExercisePlan.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'pages/exercise_dashboard.html', {'exercise_plans': exercise_plans})



@login_required(login_url="/login/")
def add_exercise_plan(request):
    if not request.user.is_Coach:
        return redirect('exercise_dashboard')

    if request.method == 'POST':
        form = ExercisePlanForm(request.POST,current_user=request.user)
        if form.is_valid():
            exercise_plan = form.save(commit=False)
            exercise_plan.coach = request.user
            exercise_plan.save()
            return redirect('exercise_dashboard')
    else:
        form = ExercisePlanForm(current_user=request.user)

    return render(request, 'pages/add_exercise_plan.html', {'form': form})

@login_required(login_url="/login/")
def generate_exercise_pdf(exercise_plan):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Add Logo at the top of the page
    logo_url = "./core/static/assets/img/brand/logob.png"
    logo_width = 50
    logo_height = 50
    p.drawImage(logo_url, 50, height - logo_height - 10, width=logo_width, height=logo_height)
    
    # Set up fonts and font sizes
    p.setFont("Helvetica-Bold", 14)
    
    # Title Section
    p.drawString(150, height - 80, f"Exercise Plan for {exercise_plan.user.username}")
    p.setFont("Helvetica", 10)
    p.drawString(150, height - 95, f"Assigned by {exercise_plan.coach.username}")
    p.drawString(150, height - 110, f"Assigned on {exercise_plan.assigned_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Draw a line to separate the title from the content
    p.setStrokeColor(colors.black)
    p.setLineWidth(1)
    p.line(50, height - 120, width - 50, height - 120)
    
    # Add content sections with improved layout
    p.setFont("Helvetica-Bold", 12)
    y_position = height - 150  # Start position for content

    sections = [
        ("Stretching", exercise_plan.stretching),
        ("Endurance", exercise_plan.endurance),
        ("Weights", exercise_plan.weights),
        ("Sports-specific Exercises", exercise_plan.sports_specific),
    ]
    
    for section_title, content in sections:
        p.drawString(100, y_position, section_title + ":")
        text = p.beginText(100, y_position - 15)
        text.setFont("Helvetica", 10)
        text.setTextOrigin(100, y_position - 15)
        text.textLines(content if content else 'No content provided')
        p.drawText(text)
        
        y_position -= 50  # Adjust the y_position for the next section
    
    # Add extra content (AI-generated or additional details)
    y_position -= 20  # Add space before extra content
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_position, "Suggestions:")
    y_position -= 15
    p.setFont("Helvetica", 10)
    p.drawString(100, y_position, "1. Maintain a consistent training schedule to achieve optimal results.")
    y_position -= 15
    p.drawString(100, y_position, "2. Include rest days to allow muscles to recover and grow.")
    y_position -= 15
    p.drawString(100, y_position, "3. Track your progress regularly to adjust your plan as needed.")
    
    # Add footer with page number
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(100, 30, f"Page 1 - Exercise Plan for {exercise_plan.user.username}")
    
    p.showPage()
    p.save()
    
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

@login_required(login_url="/login/")
def download_exercise_pdf(request, exercise_plan_id):
    if request.user.is_Coach:
        # For Coaches and Superusers: Show all diet plans
        exercise_plan = get_object_or_404(ExercisePlan, pk=exercise_plan_id, coach=request.user)

    else:
        # For Regular Users: Show only their own diet plans
        exercise_plan = get_object_or_404(ExercisePlan, pk=exercise_plan_id, user=request.user)
    
    pdf = generate_exercise_pdf(exercise_plan)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Exercise_Plan_{exercise_plan.assigned_date}.pdf"'
    return response

@login_required(login_url="/login/")
def task_checklist(request):
    if request.method == 'POST':
        form = TaskChecklistForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_checklist')
    else:
        form = TaskChecklistForm()

    tasks = TaskChecklist.objects.filter(user=request.user)
    return render(request, 'pages/task_checklist.html', {'form': form, 'tasks': tasks})

@login_required(login_url="/login/")
def update_task_status(request, task_id):
    task = get_object_or_404(TaskChecklist, id=task_id, user=request.user)
    
    if request.method == 'POST':
        # Check for delete action
        if 'delete' in request.POST:
            task.delete()
            return redirect('task_checklist')
        
        # Handle task completion update
        completed = 'completed' in request.POST
        task.completed = completed
        task.save()

    return redirect('task_checklist')
@login_required(login_url="/login/")
def create_conversation(request, user_id):
    participant = get_object_or_404(CustomUser, id=user_id)
    conversation = Conversation.objects.create()
    print("hiisfsf")
    conversation.participants.add(request.user, participant)
    return redirect('conversation_view', conversation_id=conversation.id)
@login_required(login_url="/login/")
def conversation_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.all()
    other_participants = conversation.participants.exclude(id=request.user.id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            return redirect('conversation_view', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    return render(request, 'pages/conversation.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form,
        'other_participants': other_participants
    })

@login_required(login_url="/login/")
def start_conversation_with_coach(request):
    if request.user:
        # Get all users in the same sport
        users_in_sport = CustomUser.objects.filter(sport=request.user.sport).exclude(is_superuser=True).exclude(id=request.user.id)
        
        # Get existing conversations for the coach
        existing_conversations = Conversation.objects.filter(participants=request.user)
        for conversation in existing_conversations: 
          print("azz",conversation.id)
        # Prepare a dictionary with user_id as keys and conversation IDs as values
        conversation_dict = {}
        for conversation in existing_conversations:
            participants = conversation.participants.exclude(id=request.user.id)
            for participant in participants:
                conversation_dict[participant.id] = conversation.id
        
        context = {
            'users_in_sport': users_in_sport,
            'conversation_dict': conversation_dict
        }
    else:
        # Redirect or show an error if not a coach
        return redirect('home')
    print("s",users_in_sport)
    return render(request, 'pages/start_conversation.html', context)
@login_required(login_url="/login/")
def start_conversation_with_admin(request):
    if request.user:
        # Get all users in the same sport
        users_in_sport = CustomUser.objects.all().exclude(is_Coach=True).exclude(id=request.user.id)
        
        # Get existing conversations for the coach
        existing_conversations = Conversation.objects.filter(participants=request.user)
        for conversation in existing_conversations: 
          print("azz",conversation.id)
        # Prepare a dictionary with user_id as keys and conversation IDs as values
        conversation_dict = {}
        for conversation in existing_conversations:
            participants = conversation.participants.exclude(id=request.user.id)
            for participant in participants:
                conversation_dict[participant.id] = conversation.id
        
        context = {
            'users_in_sport': users_in_sport,
            'conversation_dict': conversation_dict
        }
    else:
        # Redirect or show an error if not a coach
        return redirect('home')
    print("s",users_in_sport)
    return render(request, 'pages/start_conversation.html', context)

@login_required(login_url="/login/")
def admin_conversations(request):
    if request.user.is_superuser:
        # Get all users in the same sport
        users_in_sport = CustomUser.objects.filter().exclude(id=request.user.id)
        
        # Get existing conversations for the coach
        existing_conversations = Conversation.objects.filter(participants=request.user)
        for conversation in existing_conversations: 
          print("azz",conversation.id)
        # Prepare a dictionary with user_id as keys and conversation IDs as values
        conversation_dict = {}
        for conversation in existing_conversations:
            participants = conversation.participants.exclude(id=request.user.id)
            for participant in participants:
                conversation_dict[participant.id] = conversation.id
        
        context = {
            'users_in_sport': users_in_sport,
            'conversation_dict': conversation_dict
        }
    else:
        # Redirect or show an error if not a coach
        return redirect('home')
    print("s",users_in_sport)
    return render(request, 'pages/coach_conversations.html', context)

@login_required(login_url="/login/")
def coach_conversations(request):
    if request.user.is_Coach:
        # Get all users in the same sport
        users_in_sport = CustomUser.objects.filter(sport=request.user.sport).exclude(id=request.user.id)
        
        # Get existing conversations for the coach
        existing_conversations = Conversation.objects.filter(participants=request.user)
        for conversation in existing_conversations: 
          print("azz",conversation.id)
        # Prepare a dictionary with user_id as keys and conversation IDs as values
        conversation_dict = {}
        for conversation in existing_conversations:
            participants = conversation.participants.exclude(id=request.user.id)
            for participant in participants:
                conversation_dict[participant.id] = conversation.id
        
        context = {
            'users_in_sport': users_in_sport,
            'conversation_dict': conversation_dict
        }
    else:
        # Redirect or show an error if not a coach
        return redirect('home')
    print("s",users_in_sport)
    return render(request, 'pages/coach_conversations.html', context)

@login_required(login_url="/login/")
def start_conversation(request, user_id):
    participant = get_object_or_404(CustomUser, id=user_id)
    conversation = Conversation.objects.create()
    print("hiisfsf")
    conversation.participants.add(request.user, participant)
    return redirect('conversation_view', conversation_id=conversation.id)
@login_required(login_url="/login/")    
def list_reflections(request, athlete_id):
    title = request.GET.get('title')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    exercise_routine_helpful = request.GET.get('exercise_routine_helpful')
    diet_plan_helpful = request.GET.get('diet_plan_helpful')
    endurance = request.GET.get('endurance')
    flexibility = request.GET.get('flexibility')
    progress = request.GET.get('progress')
    motivation = request.GET.get('motivation')

    # Filter reflections based on the provided query parameters
    reflections = WeeklyReflection.objects.filter(athlete_id=athlete_id)

    if title:
        reflections = reflections.filter(title__icontains=title)
    if start_date:
        reflections = reflections.filter(date__gte=start_date)
    if end_date:
        reflections = reflections.filter(date__lte=end_date)
    if exercise_routine_helpful:
        reflections = reflections.filter(exercise_routine_helpful=exercise_routine_helpful)
    if diet_plan_helpful:
        reflections = reflections.filter(diet_plan_helpful=diet_plan_helpful)
    if endurance:
        reflections = reflections.filter(endurance=endurance)
    if flexibility:
        reflections = reflections.filter(flexibility=flexibility)
    if progress:
        reflections = reflections.filter(progress=progress)
    if motivation:
        reflections = reflections.filter(motivation=motivation)

    context = {
        'reflections': reflections,
        'athlete': get_object_or_404(CustomUser, id=athlete_id)
    }
    return render(request, 'pages/reflection_list.html', context)
@login_required(login_url="/login/")
def reflections(request):
    # Get query parameters for filtering
    title = request.GET.get('title')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    exercise_routine_helpful = request.GET.get('exercise_routine_helpful')
    diet_plan_helpful = request.GET.get('diet_plan_helpful')
    endurance = request.GET.get('endurance')
    flexibility = request.GET.get('flexibility')
    progress = request.GET.get('progress')
    motivation = request.GET.get('motivation')

    # Filter reflections based on the provided query parameters
    reflections = WeeklyReflection.objects.filter(athlete_id=request.user.id)

    if title:
        reflections = reflections.filter(title__icontains=title)
    if start_date:
        reflections = reflections.filter(date__gte=start_date)
    if end_date:
        reflections = reflections.filter(date__lte=end_date)
    if exercise_routine_helpful:
        reflections = reflections.filter(exercise_routine_helpful=exercise_routine_helpful)
    if diet_plan_helpful:
        reflections = reflections.filter(diet_plan_helpful=diet_plan_helpful)
    if endurance:
        reflections = reflections.filter(endurance=endurance)
    if flexibility:
        reflections = reflections.filter(flexibility=flexibility)
    if progress:
        reflections = reflections.filter(progress=progress)
    if motivation:
        reflections = reflections.filter(motivation=motivation)

    context = {
        'reflections': reflections,
        'athlete': get_object_or_404(CustomUser, id=request.user.id)
    }
    return render(request, 'pages/reflection.html', context)
@login_required(login_url="/login/")
def download_reflection_pdf(request, reflection_id):
    reflection = get_object_or_404(WeeklyReflection, id=reflection_id)
    
    buffer = BytesIO()
    
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 15)
    
    # Add content to the PDF
    p.drawString(100, 750, f"Weekly Reflection Form for {reflection.athlete_id.username}")
    p.drawString(100, 735, f"Date: {reflection.date.strftime('%Y-%m-%d')}")
    p.drawString(100, 720, f"Title: {reflection.title}")
    
    text = p.beginText(100, 705)
    text.setFont("Helvetica", 10)
    text.textLines([
        f"What Went Well: {reflection.what_went_well}",
        f"Even Better If: {reflection.even_better_if}",
        f"Diet Plan Helpful: {reflection.diet_plan_helpful}",
        f"Exercise Routine Helpful: {reflection.exercise_routine_helpful}",
        f"Endurance: {reflection.endurance}",
        f"Flexibility: {reflection.flexibility}",
        f"Progress: {reflection.progress}",
        f"Motivation: {reflection.motivation}"
    ])
    p.drawText(text)
    
    p.showPage()
    p.save()
    
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Reflection_Response_{reflection.date.strftime("%Y-%m-%d")}.pdf"'
    
    return response
@login_required(login_url="/login/")
def user_list(request):
    if request.user.is_superuser:
        users_in_sport = CustomUser.objects.all().exclude(is_Coach=True).exclude(is_superuser=True)
    elif request.user.is_Coach:
        users_in_sport = CustomUser.objects.filter(sport=request.user.sport).exclude(is_Coach=True).exclude(is_superuser=True).exclude(id=request.user.id)
    else:
        return redirect('home')

    user_reflections = {user: user.reflections.all() for user in users_in_sport}

    return render(request, 'pages/user_list.html', {
        'users_in_sport': users_in_sport,
        'user_reflections': user_reflections,
    })
@login_required(login_url="/login/")
def coach_list(request):
    if request.user.is_superuser:
        users_in_sport = CustomUser.objects.all().filter(is_Coach=True)
    else:
        return redirect('home')

    user_reflections = {user: user.reflections.all() for user in users_in_sport}

    return render(request, 'pages/coach_list.html', {
        'users_in_sport': users_in_sport,
        'user_reflections': user_reflections,
    })
@login_required(login_url="/login/")
def test_reminders(request):
    today = timezone.now().date()
    coaches = CustomUser.objects.all()
    print("hi",coaches)
    Exercice_MESSAGES = [
    "Hi {coach},\n\nTime to crush your exercise goals for today! Let's do it!",
    "Hi {coach},\n\nConsistency is the key to success. Stick to your plan and see the magic happen!",
    "Hi {coach},\n\nToday is another chance to improve yourself. Follow your exercise plan!",
    "Hi {coach},\n\nDon’t skip your exercise plan. Small steps lead to big changes!",
    "Hi {coach},\n\nKeep pushing yourself today. Your effort will pay off!",
    "Hi {coach},\n\nStay disciplined and focused on your goals. Your exercise plan is the way forward!",
    "Hi {coach},\n\nEvery step you take today brings you closer to your fitness goals. Stick to your plan!",
    "Hi {coach},\n\nIt’s a great day to work on becoming your best self. Let’s get moving!",
    "Hi {coach},\n\nYour dedication is inspiring. Follow your exercise plan and inspire others too!",
    "Hi {coach},\n\nRemember, the hardest part is starting. Get going with your exercise plan!"
     ]
    DIET_MESSAGES = [
    "Hi {coach},\n\nEating healthy today sets you up for a better tomorrow. Stick to your diet plan!",
    "Hi {coach},\n\nFuel your body with the right nutrition. Don’t forget your diet plan today!",
    "Hi {coach},\n\nA strong body starts with the food you eat. Stay consistent with your diet!",
    "Hi {coach},\n\nYour diet plan is your roadmap to success. Follow it and stay on track!",
    "Hi {coach},\n\nDiscipline in your diet brings long-term results. Stay committed today!",
    "Hi {coach},\n\nHealthy eating, happy living. Follow your diet plan and feel the difference!",
    "Hi {coach},\n\nRemember, good nutrition is an investment in yourself. Stick to your plan!",
    "Hi {coach},\n\nYour body deserves the best fuel. Don’t skip your diet plan today!",
    "Hi {coach},\n\nSmall daily dietary choices create great results. Stay on your plan today!",
    "Hi {coach},\n\nLet your diet be your motivation. Stick to your plan and achieve greatness!"
    ]
    for coach in coaches:
        # Sending exercise reminder email
        exercise_plan = ExercisePlan.objects.filter(user=coach).first()
        random_message = random.choice(Exercice_MESSAGES).format(coach=coach.username)
        if exercise_plan:
            send_mail(
                subject='Daily Exercise Reminder',
                message=random_message,
                from_email='mailtrap@demomailtrap.com',
                recipient_list=[coach.email],
                fail_silently=False,
            )

        # Sending diet reminder email
        diet_plan = DietPlan.objects.filter(user=coach).first()
        random_message_diet = random.choice(DIET_MESSAGES).format(coach=coach.username)
        if diet_plan:
            send_mail(
                subject='Daily Diet Plan Reminder',
                message=random_message_diet,
                from_email='mailtrap@demomailtrap.com',
                recipient_list=[coach.email],
                fail_silently=False,
            )
            print("hi")

    return render(request, 'pages/test_reminders.html', {'message': 'Daily reminders sent!'})
@login_required(login_url="/login/")
def send_weekly_reflection_reminders(request):
    today = timezone.now().date()
    last_week = today - timedelta(days=7)

    # Get athletes who have not submitted a reflection in the last week
    athletes = CustomUser.objects.all().exclude(
        reflections__date__gte=last_week
    )
    REFLECTION_MESSAGES = [
    "Hi {athlete},\n\nIt's time to fill out your weekly reflection form. Reflect on your progress this week and think about what went well and what could be improved. Remember, reflection is key to growth!\n\nTake a moment to jot down your thoughts and set goals for the upcoming week. Your journey towards improvement starts with these small steps!",
    "Hi {athlete},\n\nIt's time to fill out your weekly reflection form. How did this week go for you? What were the highlights? What can you do differently next week to get even better?\n\nYour feedback and self-reflection help us help you achieve your goals. Let's keep moving forward together!",
    "Hi {athlete},\n\nDon't forget to fill out your weekly reflection form. Reflect on your challenges, your victories, and how you can continue improving. This form helps you stay on track towards your goals.\n\nWe believe in your progress – keep it up, and let's finish the week strong!",
    "Hi {athlete},\n\nTime to fill out your weekly reflection form! Reflect on your journey this week – your effort, challenges, and achievements. This is your chance to learn and grow.\n\nYour reflections today will help guide your progress for the week ahead!",
    "Hi {athlete},\n\nIt's reflection time! Fill out your weekly form and take a moment to evaluate how you've done this week. What are you proud of? What can be improved? Every week is a new opportunity for growth.\n\nYour thoughts matter, and they shape your path to success. Keep going strong!",
    "Hi {athlete},\n\nIt's time to fill out your weekly reflection form. This is an important opportunity to assess your progress and think about how you can keep improving. Review your achievements, and set new goals for the week ahead!\n\nRemember, small improvements each week add up to big results over time!"
    ]

    # Send reminder emails to these athletes
    for athlete in athletes:
        random_reflection_message = random.choice(REFLECTION_MESSAGES).format(athlete=athlete.username)
        send_mail(
            subject='Weekly Reflection Reminder',
            message=random_reflection_message,
            from_email='mailtrap@demomailtrap.com',
            recipient_list=[athlete.email],
            fail_silently=False,
        )
    return render(request, 'pages/test_reminders.html', {'message': 'Weekly reminders sent!'})