from django.db import models
from userprofile.models import UserProfile
from budget.models import Budget


class Share(models.Model):

    # class PrivilegeChoices(models.TextChoices):
    #     VIEW = 'View'
    #     CONTRIBUTE = 'Constribute'
    #     # BLOCKED missing - if blocked then there is so Share

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='shared_to')
    shared_budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='sharing')
    # privilege = models.CharField(max_length=80, choices=PrivilegeChoices.choices, default=PrivilegeChoices.VIEW)

    objects = models.Manager()
