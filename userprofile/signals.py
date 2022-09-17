from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import UserProfile
from django.contrib.auth.models import User
from django.utils.text import slugify

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not kwargs.get('raw'):
        # print('~~>', 'Creating userprofile', sender, instance, created, kwargs, sep=' ||| ')
        if created:
            # todo chdeck of slug unique
            slug = slugify(instance.username)
            UserProfile.objects.create(user=instance, slug=slug)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not kwargs.get('raw'):
        # print('~~>', 'Saving userprofile', sender, instance, kwargs, sep=' ||| ')
        instance.user_profile.save()
