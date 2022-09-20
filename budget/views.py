from rest_framework import viewsets
from .models import Budget, Expense, ExpenseType, Income
from .serializers import BudgetSerializer, IncomeSerializer, ExpenseSerializer, ExpenseTypeSerializer
from familybudget.pagination import StandardPagination, WidePagination
from rest_framework import permissions
from .permissions import IsBudgetOwnerOrReadOnly, IsSharedOrReadOnly

class BudgetViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsBudgetOwnerOrReadOnly]

class ExpenseTypeViewSet(viewsets.ModelViewSet):
    pagination_class = WidePagination
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class ExpenseViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSharedOrReadOnly]


class IncomeViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSharedOrReadOnly]
