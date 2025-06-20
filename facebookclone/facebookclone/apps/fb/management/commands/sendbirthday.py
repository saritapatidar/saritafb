
from django.core.management.base import BaseCommand
from datetime import date
from fb.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Send birthday emails to users whose birthday is today'

    def handle(self, *args, **kwargs):
        today = date.today()
        users = CustomUser.objects.filter(
            Date_of_birth__month=today.month,
            Date_of_birth__day=today.day
        )

        for user in users:
            send_mail(
                subject='Happy Birthday!',
                message=f"Hi {user.firstname}, Happy Birthday from the Facebook!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )

        return "birthday email send"

      