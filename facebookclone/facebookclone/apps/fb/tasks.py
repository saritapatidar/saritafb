from celery import shared_task
from time import sleep 
from django.core.mail import send_mail
from .models import CustomUser
from datetime import date
from django.conf import settings



# @shared_task
# def send_email_task(subject, message, from_email, recipient_list):
# 	send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_birthday_emails():
    today = date.today()
    users = CustomUser.objects.filter(
        Date_of_birth__month=today.month,
        Date_of_birth__day=today.day
    )

    for user in users:
        send_mail(
            subject='Happy Birthday!',
            message=f"Hi {user.firstname},\n Wishing you a very Happy Birthday! , \n From: Facebook Team",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    
    return "birthday emails sent."
