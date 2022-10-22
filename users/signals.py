from email import message
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Profile
from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect



def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            email=user.email,
            username=user.username,

            name=user.first_name,
        )
        subject = 'Welcome to MyReports'
        message = f'we are glad to you are here.\nYour username is {user.username}'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,



        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    


    if created == False:
        user.first_name = profile.name
        user.username = profile.email
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)