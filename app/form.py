from django.utils import timezone
from django import forms

from app.CompetitionModel import Competition, DietPlan, ExercisePlan, Message, Result, TaskChecklist
from app.models import WeeklyReflection
from authentication.models import CustomUser

class WeeklyReflectionForm(forms.ModelForm):
    date = forms.DateField(
        initial=timezone.now().date(), 
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select Date',
                'readonly':'true'
            }
        ),
        label='Date'
    )
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Title'
            }
        ),
        label='Title'
    )

    what_went_well = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'What went well?',
                'rows': 4
            }
        ),
        label='What went well?'
    )
    even_better_if = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Even better if',
                'rows': 4
            }
        ),
        label='Even better if'
    )

    diet_plan_helpful = forms.ChoiceField(
        choices=[('Yes', 'Yes'), ('No', 'No')],
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-check'
            }
        ),
        label='Do you think your current diet plan is helping your progress?'
    )
    exercise_routine_helpful = forms.ChoiceField(
        choices=[('Yes', 'Yes'), ('No', 'No')],
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-check'
            }
        ),
        label='Do you think your current exercise routine is helping your progress?'
    )

    endurance = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Endurance'
    )
    flexibility = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Flexibility'
    )
    progress = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Progress'
    )
    motivation = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Motivation'
    )
    class Meta:
            model = WeeklyReflection
            fields = ['date', 'title', 'what_went_well', 'even_better_if', 'diet_plan_helpful', 'exercise_routine_helpful', 'endurance', 'flexibility', 'progress', 'motivation']

class EventForm(forms.ModelForm):
    date = forms.DateTimeField(
        initial=timezone.now(),  # Default value as the current date and time
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',  # Use 'datetime-local' for both date and time selection
                'class': 'form-control form-control-alternative',
                'placeholder': 'Select Date and Time'
            }
        ),
        label='Date and Time'
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Competition Name'
            }
        ),
        label='Name'
    )

    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Location'
            }
        ),
        label='Location'
    )

    class Meta:
        model = Competition
        fields = ['name', 'date', 'location']
class ResultForm(forms.ModelForm):
    competition = forms.ModelChoiceField(
        queryset=Competition.objects.none(),  # Provide a queryset for the dropdown
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-alternative',
                'placeholder': 'Select Competition'
            }
        ),
        label='Competition'
    )

    athlete = forms.ModelChoiceField(
        queryset=CustomUser.objects.exclude(is_Coach=True).exclude(is_superuser=True),  # Provide a queryset for the dropdown
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-alternative',
                'placeholder': 'Select Athlete'
            }
        ),
        label='Athlete'
    )

    result = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-alternative',
                'placeholder': 'Enter Result'
            }
        ),
        label='Result'
    )

    class Meta:
        model = Result
        fields = ['competition', 'athlete', 'result']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter queryset for 'competition' field to show only past competitions
        self.fields['competition'].queryset = Competition.objects.filter(date__lt=timezone.now())

class DietPlanForm(forms.ModelForm):
    class Meta:
        model = DietPlan
        fields = ['user','breakfast', 'lunch', 'snack', 'dinner']
        widgets = {
            'breakfast': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe breakfast'}),
            'lunch': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe lunch'}),
            'snack': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe snack'}),
            'dinner': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe dinner'}),
        }

    def __init__(self, *args, **kwargs):
        # Get the current user from the kwargs
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        if current_user:
            # Filter users based on the sport of the current user
            self.fields['user'].queryset = CustomUser.objects.exclude(is_Coach=True).exclude(is_superuser=True).filter(sport=current_user.sport)
        else:
            # Optionally handle the case where current_user is not provided
            self.fields['user'].queryset = CustomUser.objects.none()

class ExercisePlanForm(forms.ModelForm):
    class Meta:
        model = ExercisePlan
        fields = ['user','stretching', 'endurance', 'weights', 'sports_specific']
        widgets = {
            'stretching': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe stretching exercises'}),
            'endurance': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe endurance exercises'}),
            'weights': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe weight exercises'}),
            'sports_specific': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe sports-specific exercises'}),
        }

    def __init__(self, *args, **kwargs):
        # Get the current user from the kwargs
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        if current_user:
            # Filter users based on the sport of the current user
            self.fields['user'].queryset = CustomUser.objects.exclude(is_Coach=True).exclude(is_superuser=True).filter(sport=current_user.sport)
        else:
            # Optionally handle the case where current_user is not provided
            self.fields['user'].queryset = CustomUser.objects.none()            
class TaskChecklistForm(forms.ModelForm):
    class Meta:
        model = TaskChecklist
        fields = ['task']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']