from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BudgetViewSet, ExpenseViewSet, ExpenseTypeViewSet, IncomeViewSet

app_name = 'budget'
router = DefaultRouter()
router.register(r'budget', BudgetViewSet, basename='budget')
router.register(r'expensetype', ExpenseTypeViewSet, basename='expensetype')
router.register(r'expense', ExpenseViewSet, basename='expense')
router.register(r'income', IncomeViewSet, basename='income')

urlpatterns = [
              ] + router.urls
