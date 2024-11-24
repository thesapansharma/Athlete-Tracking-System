from django.core.mail import send_mail
import random

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp}',
        'no-reply@example.com',  # Replace with your email
        [email],
        fail_silently=False,
    )
    return otp