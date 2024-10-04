import os
import json
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from users.models import User
from datetime import datetime


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    if kwargs['created']:
        subject = 'User joined'
        message = f'{instance.username} joined.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all() if user.is_superuser]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=User)
def pre_delete_customer(sender, instance, **kwargs):
    user_data = {
        'id': instance.id,
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'email': instance.email,
        'username': instance.username,
        'phone number': str(instance.phone_number),
        'image': str(instance.image),
        'data_joined': str(instance.data_joined),
        'is_active': str(instance.is_active),
        'is_stuff': str(instance.is_staff),
        'is_superuser': str(instance.is_superuser),
    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'users/deleted_data/deleted_users', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(user_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
