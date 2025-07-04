from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from fb.models import CustomUser
from django.conf import settings

class Command(BaseCommand):
    help = 'Send emails to inactive users and delete accounts inactive for over 1 year'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        six_months_ago = now - timedelta(days=5/1440)
        one_year_ago = now - timedelta(days=15)

        six_months_inactive_users = CustomUser.objects.filter(last_login__lt=six_months_ago, last_login__gte=one_year_ago)

        for user in six_months_inactive_users:
            if user.email:
                send_mail(
                    subject='We miss you at Facebook!',
                    message=f"Hi {user.firstname},\n\nWe've noticed you haven't logged in for a while. Are you still interested in Facebook?\n\nCome back and see what your friends are up to!\n\n If you are not login then we will delete your accounts on 15 days!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False
                )

                
        one_year_inactive_users = CustomUser.objects.filter(last_login__lt=one_year_ago)

        for user in one_year_inactive_users:
            user.delete()
           

        return "done"


