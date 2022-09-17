from django.contrib import admin
from .models import Budget, Expense, ExpenseType, Income

admin.site.register(Budget)
admin.site.register(ExpenseType)
admin.site.register(Expense)
admin.site.register(Income)