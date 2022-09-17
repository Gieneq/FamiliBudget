from django.db import models
from userprofile.models import UserProfile
from datetime import date
from djmoney.models.fields import MoneyField

class Budget(models.Model):
    owners_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='budgets_created')
    date_year_month = models.DateField(auto_now_add=True)


class ExpenseType(models.Model):

    class ExpenseChoices(models.TextChoices):
        FOOD = 'Food'
        FUN = 'Fun'
        CLOTHES = 'Clothes'
        EATING_OUT = 'Eating out'
        CAR_COMMUNICATION = 'Car/Communication'
        RENT_MORTGAGE = 'Rent/Mortgage'
        WATER_BILL = 'Water Bill'
        ELECTRIC_BILL = 'Electric Bill'
        INTERNET_BILL = 'Internet Bill'
        PHONE_BILL = 'Phone Bill'
        LOANS = 'Loans'
        COSMETICS = 'Cosmetics'
        HEALTH = 'Health'

    name = models.CharField(max_length=80, choices=ExpenseChoices.choices, default=ExpenseChoices.FOOD, unique=True)

    def __str__(self):
        return f"ExpenseType: {self.name}"

class Expense(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='expenses_made')
    budget_common = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expenses_contributed')
    date = models.DateField(auto_now_add=True)
    type = models.ForeignKey(ExpenseType, on_delete=models.SET_NULL, null=True, related_name='examples')
    value = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN')

    def __str__(self):
        return f"Expense of: {self.value}"

class Income(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='incomes_made')
    budget_common = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='incomes_contributed')
    value = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN')

    def __str__(self):
        return f"Income of: {self.value}"
