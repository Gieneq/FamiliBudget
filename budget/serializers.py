from rest_framework import serializers
from rest_framework.reverse import reverse
from userprofile.serializers import UserProfileSerializer

from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    # url = serializers.SerializerMethodField(read_only=True)
    # profile = UserProfileSerializer()
    owners_profile = UserProfileSerializer()

    class Meta:
        model = Budget
        fields = '__all__'

    # def get_url(self, instance):
    #     request = self.context.get('request')
    #     return reverse('share:share-detail', args=[instance.pk], request=request)