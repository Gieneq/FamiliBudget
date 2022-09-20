from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from django.utils.text import slugify
from budget.serializers import IncomeLinkSerializer, ExpenseLinkSerializer, BudgetLinkSerializer


class SimpleUserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'url']

    def get_url(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:user_detail', args=[instance.user_profile.slug], request=request)


class SimpleUserProfileSerializer(serializers.ModelSerializer):
    # url = serializers.URLField(source='absolute_url', read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['slug', 'url']

    def get_url(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:userprofile_detail', args=[instance.slug], request=request)


# usable below

class UserSerializer(serializers.ModelSerializer):
    user_profile = SimpleUserProfileSerializer(many=False, read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    url_delete = serializers.SerializerMethodField(read_only=True)
    url_edit = serializers.SerializerMethodField(read_only=True)
    url_edit_password = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'url', 'url_edit', 'url_edit_password', 'url_delete', 'user_profile']

    def get_url(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:user_detail', args=[instance.user_profile.slug], request=request)

    def get_url_edit(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:user_edit', args=[instance.user_profile.slug], request=request)

    def get_url_delete(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:user_delete', args=[instance.user_profile.slug], request=request)

    def get_url_edit_password(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:user_editpassword', args=[instance.user_profile.slug], request=request)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

        extra_kwargs = {
            'password2': {'write_only': True}
        }

    def save(self, **kwargs):
        val_data = self.validated_data
        pass1 = val_data.get('password')
        pass2 = val_data.pop('password2')
        if pass1 != pass2:
            raise ValidationError(f"Passwords not equal. {pass1} is not {pass2}")
        return User.objects.create_user(**val_data)


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        new_slug = slugify(validated_data['username'])
        instance_updated = super().update(instance, validated_data)
        instance_updated.user_profile.slug = new_slug
        print('Slug changed to:', instance_updated.user_profile.slug)
        instance_updated.user_profile.save()
        return instance_updated


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password_old = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    password = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['password_old', 'password', 'password2']

        extra_kwargs = {
            'password_old': {'write_only': True},
            'password2': {'write_only': True},
        }

    def update(self, instance, validated_data):
        pass_old = validated_data['password_old']
        if not instance.check_password(pass_old):
            raise ValidationError(f"Passwords for {instance.username} is incorrect.")

        pass1 = validated_data['password']
        pass2 = validated_data['password2']
        if pass1 != pass2:
            raise ValidationError(f"Passwords not equal. {pass1} is not {pass2}")
        instance.set_password(pass1)
        instance.save()
        return instance


class UserDestroySerializer():
    password2 = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'url', 'email']
        lookup_field = 'user_profile__slug'

        extra_kwargs = {
            # 'url': {'lookup_field': 'user_profile__slug'},
            'password2': {'write_only': True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    url_budgets = serializers.SerializerMethodField(read_only=True)
    user_url = serializers.SerializerMethodField(read_only=True)

    # user = SimpleUserSerializer(many=False, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['slug', 'url', 'url_budgets', 'user', 'user_url']

    def get_url(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:userprofile_detail', args=[instance.slug], request=request)

    def get_user_url(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:user_detail', args=[instance.slug], request=request)

    def get_url_budgets(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:userprofile_budget_detail', args=[instance.slug], request=request)


class UserProfileBudgetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    url_shared_to = serializers.SerializerMethodField(read_only=True)
    incomes_made = IncomeLinkSerializer(many=True)
    expenses_made = ExpenseLinkSerializer(many=True)
    budgets_created = BudgetLinkSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ['url', 'url_shared_to', 'incomes_made', 'expenses_made', 'budgets_created']

    def get_url(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:userprofile_detail', args=[instance.slug], request=request)

    def get_url_shared_to(self, instance):
        request = self.context.get('request')
        return reverse('share:share_query', request=request) + f'?slug={instance.slug}'
