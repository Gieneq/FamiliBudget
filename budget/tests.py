from django.test import TestCase
from .models import Budget, ExpenseType, Expense, Income
from userprofile.models import UserProfile
from django.contrib.auth.models import User
from datetime import date
from djmoney.money import Money
from django.core.exceptions import ValidationError
from functools import reduce
from operator import add

class ExpenseTypeTestCase(TestCase):

    def test_expense_type(self):
        expense_type1 = ExpenseType.objects.create(name=ExpenseType.ExpenseChoices.CAR_COMMUNICATION)
        # print(et1.name)
        # print(et1.name in ExpenseType.ExpenseChoices.labels)
        # print(ExpenseType.ExpenseChoices.labels)

        self.assertIn(expense_type1.name, ExpenseType.ExpenseChoices.labels)

class BudgetManagementTestCase(TestCase):
    def setUp(self):
        for expense_type_choice in ExpenseType.ExpenseChoices.labels:
            ExpenseType.objects.create(name=expense_type_choice)

        # ExpenseType.objects.create()
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

    def test_budget_creation(self):
        self.assertEqual(self.date_b1.strftime("%Y.%m"), '2022.09')
        b1_reverse = self.user1.user_profile.budgets_created.first()
        self.assertEqual(self.budget1, b1_reverse)
        self.assertEqual(self.budget1.date_year_month, self.date_b1)

    def test_budget_creation_date(self):
        date_b = date(2022, 9, 12)
        budget = Budget.objects.create(owners_profile=self.user1.user_profile, date_year_month=date_b)
        self.assertEqual(budget.date_year_month.day, 1)

    def test_budget_empty(self):
        self.assertEqual(Money(0, 'PLN'), self.budget1.summarise_incomes)
        self.assertEqual(Money(0, 'PLN'), self.budget1.summarise_expenses)
        self.assertEqual(Money(0, 'PLN'), self.budget1.summarise_all)

    def test_budget_only_income(self):
        income_value = Money(15000, 'PLN')
        income1 = Income.objects.create(profile=self.user2.user_profile, budget_common=self.budget1, value=income_value)
        self.assertEqual(income_value, self.budget1.summarise_incomes)
        self.assertEqual(Money(0, 'PLN'), self.budget1.summarise_expenses)
        self.assertEqual(income_value, self.budget1.summarise_all)
        self.assertEqual(income_value, income1.value)

    def test_budget_only_expenses(self):
        expense_value1 = Money(1500, 'PLN')
        date_expense1 = date(2022, 9, 5)
        expense1 = Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date_expense1, value=expense_value1,
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.FOOD))

        self.assertEqual(Money(0, 'PLN'), self.budget1.summarise_incomes)
        self.assertEqual(expense_value1, self.budget1.summarise_expenses)
        self.assertEqual(-expense_value1, self.budget1.summarise_all)
        self.assertEqual(expense_value1, expense1.value)


    def test_budget_only_expenses_more(self):
        expense_value1 = Money(1500, 'PLN')
        date_expense1 = date(2022, 9, 5)
        expense1 = Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date_expense1, value=expense_value1,
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.FOOD))


        expense_value2 = Money(2500, 'PLN')
        date_expense2 = date(2022, 9, 12)
        expense2 = Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date_expense2, value=expense_value2,
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.CAR_COMMUNICATION))


        self.assertEqual(Money(0, 'PLN'), self.budget1.summarise_incomes)
        self.assertEqual(expense_value1+expense_value2, self.budget1.summarise_expenses)
        self.assertEqual(-expense_value1-expense_value2, self.budget1.summarise_all)


    def test_budget_expenses_sum_incomes(self):
        income_value = Money(15000, 'PLN')
        income1 = Income.objects.create(profile=self.user2.user_profile, budget_common=self.budget1, value=income_value)
        self.assertEqual(self.budget1.incomes_contributed.first().value, income_value)

        expense_value1 = Money(1500, 'PLN')
        date_expense1 = date(2022, 9, 5)
        expense1 = Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date_expense1, value=expense_value1,
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.FOOD))

        expense_value2 = Money(2500, 'PLN')
        date_expense2 = date(2022, 9, 12)
        expense2 = Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date_expense2, value=expense_value2,
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.CAR_COMMUNICATION))

        expense_value3 = Money(1200, 'PLN')
        date_expense3 = date(2022, 9, 16)
        expense2 = Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date_expense3, value=expense_value3,
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.CLOTHES))

        self.assertEqual(self.budget1.expenses_contributed.count(), 3)

        expenses_sum = expense_value1 + expense_value2 + expense_value3
        self.assertEqual(income_value, self.budget1.summarise_incomes)
        self.assertEqual(expenses_sum, self.budget1.summarise_expenses)
        self.assertEqual(income_value-expenses_sum, self.budget1.summarise_all)



    def test_budget_outdated_expense(self):
        income_value = Money(15000, 'PLN')
        income1 = Income.objects.create(profile=self.user2.user_profile, budget_common=self.budget1, value=income_value)
        self.assertEqual(self.budget1.incomes_contributed.first().value, income_value)

        expense_value1 = Money(1500, 'PLN')
        date_expense1 = date(2022, 10, 5)

        with self.assertRaises(ValidationError):
            Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date_expense1, value=expense_value1,
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.FOOD))


        self.assertEqual(income_value, self.budget1.summarise_incomes)
        self.assertEqual(Money(0, 'PLN'), self.budget1.summarise_expenses)
        self.assertEqual(income_value, self.budget1.summarise_all)


    def test_budget_sort_by_expenses_type(self):
        expense1_food = Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date(2022, 9, 5), value=Money(1500, 'PLN'),
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.FOOD))

        expense2_health = Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date(2022, 9, 5), value=Money(1500, 'PLN'),
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.HEALTH))
        expense3_food = Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date(2022, 9, 5), value=Money(1500, 'PLN'),
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.FOOD))

        expense4_food = Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date(2022, 9, 5), value=Money(1500, 'PLN'),
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.FOOD))
        expense5_health = Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date(2022, 9, 5), value=Money(1500, 'PLN'),
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.HEALTH))
        expense6_car = Expense.objects.create(profile=self.user2.user_profile, budget_common=self.budget1,
                                          date=date(2022, 9, 5), value=Money(1500, 'PLN'),
                                          type=ExpenseType.objects.get(name=ExpenseType.ExpenseChoices.CAR_COMMUNICATION))

        def aggregate_expenses_type(*expenses):
            count = len(expenses)
            val_sum = reduce(add, map(lambda x: x.value, expenses))
            return count, val_sum

        food_expenses_count, food_expenses_sum = aggregate_expenses_type(expense1_food, expense3_food, expense4_food)
        health_expenses_count, health_expenses_sum = aggregate_expenses_type(expense2_health, expense5_health)
        car_expenses_count, car_expenses_sum = aggregate_expenses_type(expense6_car)

        expenses_sorted = self.budget1.sort_by_expenses_type
        print(expenses_sorted)
        self.assertEqual(len(expenses_sorted), 3)

        expenses_sorted_food = expenses_sorted.filter(type__name=ExpenseType.ExpenseChoices.FOOD).first()
        self.assertEqual(expenses_sorted_food['type_count'], food_expenses_count)
        self.assertEqual(expenses_sorted_food['value_sum'], food_expenses_sum.amount)

        expenses_sorted_health = expenses_sorted.filter(type__name=ExpenseType.ExpenseChoices.HEALTH).first()
        self.assertEqual(expenses_sorted_health['type_count'], health_expenses_count)
        self.assertEqual(expenses_sorted_health['value_sum'], health_expenses_sum.amount)

        expenses_sorted_car = expenses_sorted.filter(type__name=ExpenseType.ExpenseChoices.CAR_COMMUNICATION).first()
        self.assertEqual(expenses_sorted_car['type_count'], car_expenses_count)
        self.assertEqual(expenses_sorted_car['value_sum'], car_expenses_sum.amount)
