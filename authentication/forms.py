# -*- encoding: utf-8 -*-


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from authentication.models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",                
                "class": "form-control"
            }
        ))
    birth_date = forms.DateField(required=False, input_formats=['%Y-%m-%d'])
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",                
                "class": "form-control"
            }
        ))
    sport = forms.ChoiceField(
        choices=CustomUser.SPORT_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        ))
    is_Coach = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check"
            }
        ))
    otp = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter OTP",
                "class": "form-control",
                "style": "display: none;"  # Initially hidden
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'birth_date', 'sport', 'is_Coach', 'otp')
class UserProfileForm(forms.ModelForm):
    sport = forms.ChoiceField(
        choices=CustomUser.SPORT_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-alternative"
            }
        )
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-alternative"
            }
        )
    )
    
    photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control form-control-alternative"
            }
        )
    )
    
    identification = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control form-control-alternative"
            }
        )
    )
    
    height = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-alternative"
            }
        )
    )
    
    weight = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-alternative"
            }
        )
    )
    
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-alternative"
            }
        )
    )
    
    father_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-alternative"
            }
        )
    )
    
    father_phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-alternative"
            }
        )
    )
    
    mother_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-alternative"
            }
        )
    )
    
    mother_phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-alternative"
            }
        )
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'sport',
            'phone_number',
            'photo',
            'identification',
            'height',
            'weight',
            'gender',
            'father_name',
            'father_phone_number',
            'mother_name',
            'mother_phone_number',
        ]