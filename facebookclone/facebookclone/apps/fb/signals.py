from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Comment,CreatePost
import os
from django.core.mail import send_mail


@receiver(post_save, sender=Comment)
def send_thanks_on_reply(sender, instance, created, **kwargs):
    if created and instance.parent:
        user_email = instance.user.email
        if user_email:
            try:
                send_mail(
                    subject="Thanks for your Reply !",
                    message=f"Thank you {instance.user.firstname} for replying!",
                    from_email="saritapatidar@thoughtwin.com",
                    recipient_list=[user_email],
                    fail_silently=False
                )
                print("MAIL IS SENT")
            except Exception as e:
                print("MAIL DO NOT send:", e)


# @receiver(post_delete,sender=CreatePost)
# def delete_post_images(sender,instance,**kwargs):
# 	if instance.image:
# 		if os.path.isfile(instance.image.path):
# 			os.remove(instance.image.path)
# 			print(f"{instance.user.user.firstname}  your image is Deleted!")








	