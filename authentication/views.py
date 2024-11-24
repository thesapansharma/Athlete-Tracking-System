# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

import random
from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from app.CompetitionModel import Competition, Result
from .forms import LoginForm, SignUpForm, UserProfileForm
from django.contrib.auth import get_user_model
User = get_user_model() 
def login_view(request):
    form = LoginForm(request.POST or None)

    msg = 'Sign in with credentials'

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import SignUpForm
from .utils import send_otp

def register_user(request):
    step = request.session.get('registration_step', 1)  # Default to Step 1
    msg = 'Add your credentials'
    form = SignUpForm()  # Default initialization of the form

    if request.method == "POST":
        if step == 1:  # Step 1: Handle form submission and send OTP
            form = SignUpForm(request.POST, request.FILES)  # Reinitialize with POST data
            if form.is_valid():
                email = form.cleaned_data.get("email")
                otp_code = send_otp(email)  # Send OTP to the email
                request.session['otp'] = otp_code
                request.session['email_for_otp'] = email
                request.session['registration_step'] = 2  # Move to Step 2
                request.session['registration_form_data'] = request.POST  # Save form data for Step 2
                msg = f"An OTP has been sent to {email}. Please enter it to complete your registration."
                messages.info(request, msg)
                return redirect(request.path)  # Redirect to refresh and reflect Step 2
            else:
                msg = 'Form is not valid'
                messages.error(request, msg)

        elif step == 2:  # Step 2: Handle OTP verification and resend OTP
            if 'resend_otp' in request.POST:  # Handle Resend OTP button
                email = request.session.get('email_for_otp')
                if email:
                    otp_code = send_otp(email)  # Send a new OTP
                    request.session['otp'] = otp_code  # Update the session with the new OTP
                    msg = f"A new OTP has been sent to {email}."
                    messages.info(request, msg)
                else:
                    msg = "Unable to resend OTP. Please restart the registration process."
                    messages.error(request, msg)
            else:  # Handle OTP submission
                otp = request.POST.get("otp", None)
                stored_otp = request.session.get("otp", None)
                if otp and otp == stored_otp:  # Validate OTP
                    email = request.session.get('email_for_otp')
                    form_data = request.session.get('registration_form_data')
                    form = SignUpForm(form_data)  # Retrieve initial form data
                    if form.is_valid():
                        user = form.save(commit=False)  # Save user data
                        user.save()
                        messages.success(request, "Registration successful. Please log in.")
                        # Clear session data
                        for key in ['otp', 'email_for_otp', 'registration_step', 'registration_form_data']:
                            request.session.pop(key, None)
                        return redirect("/login/")
                else:
                    msg = 'Invalid OTP.'
                    messages.error(request, msg)

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "step": step})

def send_otp(email):
    otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
    send_mail(
        'Password Reset OTP',
        f'Your OTP for password reset is {otp}.',
        'noreply@yourdomain.com',
        [email],
        fail_silently=False,
    )
    return otp

# Request Password Reset
def request_password_reset(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            # Look up user by username
            user = User.objects.get(username=username)  # Use CustomUser model
            otp = send_otp(user.email)  # Send OTP to the user's email
            request.session['reset_username'] = username
            request.session['reset_otp'] = otp
            messages.info(request, f"An OTP has been sent to {user.email}.")
            return redirect('verify_otp')  # Redirect to OTP verification page
        except User.DoesNotExist:
            messages.error(request, "No user found with this username.")
    
    return render(request, "accounts/request_password_reset.html")

# Verify OTP
def verify_otp(request):
    msg = ""
    if request.method == "POST":
        otp = request.POST.get("otp")
        stored_otp = request.session.get("reset_otp")
        
        if otp == stored_otp:
            msg ="OTP verified. Please set a new password."
            return redirect('set_new_password')  # Redirect to set new password page
        else:
            msg="Invalid OTP. Please try again."
    
    # Resend OTP if needed
    if request.GET.get("resend") == "true":
        username = request.session.get("reset_username")
        user = User.objects.get(username=username)  # Use CustomUser model
        new_otp = send_otp(user.email)  # Send a new OTP
        request.session['reset_otp'] = new_otp
        msg=f"A new OTP has been sent to {user.email}."
    
    return render(request, "accounts/verify_otp.html", {'msg': msg})

# Set New Password
def set_new_password(request):
    msg = ""
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        username = request.session.get("reset_username")

        if password != confirm_password:
            msg="Passwords do not match."
        else:
            try:
                user = User.objects.get(username=username)  # Use CustomUser model
                user.password = make_password(password)  # Save hashed password
                user.save()
                msg="Password reset successful. Please log in."
                # Clear session data
                for key in ['reset_username', 'reset_otp']:
                    request.session.pop(key, None)
                return redirect('login')
            except User.DoesNotExist:
                msg="Error resetting password. Please try again."
    
    return render(request, "accounts/set_new_password.html", {'msg': msg})

def logout_user(request):

    request.session.clear()
    return redirect('login')
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to a profile view or success page
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'pages/profile.html', {'form': form})

