from rest_framework import serializers
from rest_framework.reverse import reverse
from userprofile.serializers import UserProfileSerializer
from budget.serializers import BudgetSerializer
from .models import Share


class ShareSimpleSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    profile_url = serializers.SerializerMethodField(read_only=True)
    # shared_budget = BudgetSerializer()

    class Meta:
        model = Share
        fields = '__all__'

    def get_url(self, instance):
        request = self.context.get('request')
        return reverse('share:share-detail', args=[instance.pk], request=request)
    def get_profile_url(self, instance):
        request = self.context.get('request')
        return reverse('userprofile:userprofile_detail', args=[instance.profile.slug], request=request)