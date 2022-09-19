from rest_framework import viewsets
from .models import Budget, Expense, ExpenseType, Income
from .serializers import BudgetSerializer, IncomeSerializer, ExpenseSerializer, ExpenseTypeSerializer
from familybudget.pagination import StandardPagination, WidePagination


class BudgetViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

class ExpenseTypeViewSet(viewsets.ModelViewSet):
    pagination_class = WidePagination
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class IncomeViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
