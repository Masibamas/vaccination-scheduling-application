import os 
from django.dispatch import receiver
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

@receiver(models.signals.pre_save, sender = User)
def auto_delete_file_on_change(sender, instance, **kwargs):

    try: 
        old_image = User.objects.get(pk=instance.pk).photo
    except User.DoesNotExist:
        return False
    
    new_image = instance.photo

    if bool(old_image) and new_image != old_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)