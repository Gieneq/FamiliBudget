from django.core.exceptions import ValidationError
from django.db import models
from userprofile.models import UserProfile
from datetime import date
from dateutil import relativedelta
from djmoney.models.fields import MoneyField
from django.db.models import Sum, Count, F
from djmoney.money import Money

class Budget(models.Model):
    owners_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='budgets_created')
    date_year_month = models.DateField(default=date.today)

    objects = models.Manager()

    @property
    def summarise_expenses(self):
        if self.expenses_contributed.exists():
            return Money(self.expenses_contributed.all().aggregate(Sum('value'))['value__sum'], 'PLN')
        return Money(0, 'PLN')

    @property
    def summarise_incomes(self):
        if self.incomes_contributed.exists():
            return Money(self.incomes_contributed.all().aggregate(Sum('value'))['value__sum'], 'PLN')
        return Money(0, 'PLN')

    @property
    def summarise_all(self):
        return self.summarise_incomes - self.summarise_expenses

    @property
    def sort_by_expenses_type(self):
        return self.expenses_contributed.values('type').order_by('type').annotate(type_count=Count('type')).annotate(value_sum=Sum('value'))

    def save(self, *args, **kwargs):
        if(self.date_year_month.day != 1):
            self.date_year_month = date(self.date_year_month.year, self.date_year_month.month, 1)
        return super().save(*args, **kwargs)

    # todo zrob jakos wykaz wydatow per kategoria

class ExpenseType(models.Model):

    class ExpenseChoices(models.TextChoices):
        FOOD = 'Food'
        FUN = 'Fun'
        CLOTHES = 'Clothes'
        EATING_OUT = 'Eating out'
        CAR_COMMUNICATION = 'Car Communication'
        RENT_MORTGAGE = 'Rent Mortgage'
        WATER_BILL = 'Water Bill'
        ELECTRIC_BILL = 'Electric Bill'
        INTERNET_BILL = 'Internet Bill'
        PHONE_BILL = 'Phone Bill'
        LOANS = 'Loans'
        COSMETICS = 'Cosmetics'
        HEALTH = 'Health'

    name = models.CharField(max_length=80, choices=ExpenseChoices.choices, default=ExpenseChoices.FOOD, unique=True)

    objects = models.Manager()

    def __str__(self):
        return f"ExpenseType: {self.name}"

class Expense(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='expenses_made')
    budget_common = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expenses_contributed')
    date = models.DateField(default=date.today)
    type = models.ForeignKey(ExpenseType, on_delete=models.SET_NULL, null=True, related_name='examples')
    value = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN')

    objects = models.Manager()

    def save(self, *args, **kwargs):
        # print(args, kwargs, self)
        def in_month_range(date_of, date_starting):
            date_ending = date_starting + relativedelta.relativedelta(months=1)
            return date_starting <= date_of < date_ending

        if in_month_range(self.date, self.budget_common.date_year_month):
            return super().save(*args, **kwargs)
        raise ValidationError(f"Expenses for month {self.date.month} cannot be applied to budget of month {self.budget_common.date_year_month.month}")


    def __str__(self):
        return f"Expense of: {self.value} at {self.date} type: {self.type}"

class Income(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='incomes_made')
    budget_common = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='incomes_contributed')
    value = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN', default=0)

    objects = models.Manager()

    def __str__(self):
        return f"Income of: {self.value}"
