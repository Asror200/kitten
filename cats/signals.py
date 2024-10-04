import os
import json
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from cats.models import Cat, Comment
from datetime import datetime
from users.models import User


@receiver(post_save, sender=Cat)
def create_user_profile(sender, instance, **kwargs):
    if kwargs['created']:
        subject = 'A new cat was added'
        message = f'{instance.name} was added by {instance.user.username}.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all() if user.email and user.cats.breed == instance.breed]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Cat)
def pre_delete_customer(sender, instance, **kwargs):
    user_data = {
        'id': instance.id,
        'name': instance.name,
        'breed': instance.breed.name,
        'date_of_birth': str(instance.date_of_birth),
        'about': instance.about,
        'color': instance.color,
        'owner': instance.user.username,
    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'cats/deleted_data/deleted_cats', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(user_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


@receiver(post_save, sender=Comment)
def create_user_profile(sender, instance, **kwargs):
    if kwargs['created']:
        subject = 'A new comment was added'
        message = f'{instance.first_name} was added by {instance.user.username}.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all() if user.cats == instance.cat and user.email]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Comment)
def pre_delete_customer(sender, instance, **kwargs):
    user_data = {
        'id': instance.id,
        'text': instance.text,
        'cat': instance.cat.name,
        'username': instance.user.username,


    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'cats/deleted_data/deleted_comments', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(user_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
