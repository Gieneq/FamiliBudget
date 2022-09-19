from django.test import TestCase
from budget.models import Budget, ExpenseType, Expense, Income
from userprofile.models import UserProfile
from django.contrib.auth.models import User
from datetime import date
from djmoney.money import Money
from django.core.exceptions import ValidationError
from functools import reduce
from operator import add
from .models import Share

class ExpenseTypeTestCase(TestCase):

    def setUp(self):
        for expense_type_choice in ExpenseType.ExpenseChoices.labels:
            ExpenseType.objects.create(name=expense_type_choice)
        self.user1 = User.objects.create_user('Testcaser1', 'test')
        self.user2 = User.objects.create_user('Testcaser2', 'test')
        self.user3 = User.objects.create_user('Testcaser3', 'test')
        self.date_b1 = date(2022, 9, 1)
        self.budget1 = Budget.objects.create(owners_profile=self.user1.user_profile, date_year_month=self.date_b1)

    def tearDown(self):
        ExpenseType.objects.all().delete()
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()
        self.budget1.delete()

    def test_share(self):
        pass