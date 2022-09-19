from django.db import models


class Share(models.Model):
    class PrivilegeChoices(models.TextChoices):
        VIEW = 'View'
        EDIT = 'Edit'

    profile = models.ForeignKey('userprofile.UserProfile', on_delete=models.CASCADE, related_name='shared_to')
    shared_budget = models.ForeignKey('budget.Budget', on_delete=models.CASCADE, related_name='sharing')
    privilege = models.CharField(max_length=8, choices=PrivilegeChoices.choices, default=PrivilegeChoices.VIEW)

    objects = models.Manager()
