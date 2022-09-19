from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Budget, Expense, ExpenseType, Income


class BudgetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    owners_profile_url = serializers.SerializerMethodField(read_only=True)

    # sum_expenses = serializers.SerializerMethodField(read_only=True)
    # sum_income = serializers.SerializerMethodField(read_only=True)
    # sum_all = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Budget
        fields = '__all__'

    def get_url(self, instance):
        request = self.context.get('request')
        return reverse('budget:budget-detail', args=[instance.pk], request=request)

    def get_owners_profile_url(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:userprofile_detail', args=[instance.owners_profile.slug], request=request)

    # def get_sum_expenses(self, instance):
    #     return instance.summarise_expenses
    #
    #
    # def get_sum_income(self, instance):
    #     return instance.summarise_incomes
    #
    #
    # def get_sum_all(self, instance):
    #     return instance.summarise_all


class ExpenseTypeSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ExpenseType
        fields = '__all__'

    def get_url(self, instance):
        request = self.context.get('request')
        return reverse('budget:expensetype-detail', args=[instance.pk], request=request)


class ExpenseSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    profile_url = serializers.SerializerMethodField(read_only=True)
    budget_url = serializers.SerializerMethodField(read_only=True)
    type_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'

    def get_url(self, instance):
        request = self.context.get('request')
        return reverse('budget:expense-detail', args=[instance.pk], request=request)

    def get_profile_url(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:userprofile_detail', args=[instance.profile.slug], request=request)

    def get_budget_url(self, instance):
        request = self.context.get('request')
        return reverse('budget:budget-detail', args=[instance.budget_common.pk], request=request)

    def get_type_url(self, instance):
        request = self.context.get('request')
        return reverse('budget:expensetype-detail', args=[instance.type.pk], request=request)


class IncomeSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    profile_url = serializers.SerializerMethodField(read_only=True)
    budget_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Income
        fields = '__all__'

    def get_url(self, instance):
        request = self.context.get('request')
        return reverse('budget:income-detail', args=[instance.pk], request=request)

    def get_profile_url(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:userprofile_detail', args=[instance.profile.slug], request=request)

    def get_budget_url(self, instance):
        request = self.context.get('request')
        return reverse('budget:budget-detail', args=[instance.budget_common.pk], request=request)
