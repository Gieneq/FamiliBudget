from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.reverse import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    slug = models.SlugField(max_length=200, unique=True)

    objects = models.Manager()

    def __str__(self):
        return f"Profile of: {self.user.username}"

    @property
    def relative_url(self):
        return reverse('userprofile:userprofile_detail', args=[self.slug])
