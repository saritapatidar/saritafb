from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import CreatePost
import os

@receiver(post_delete,sender=CreatePost)
def delete_post_images(sender,instance,**kwargs):
	if instance.image:
		if os.path.isfile(instance.image.path):
			os.remove(instance.image.path)
			print(f"{instance.user.user.firstname}  your image is Deleted!")




	