from django.db.models import fields
from rest_framework import serializers
from ads.models import Ads 


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads 
        fields = ('id', 'orgname','weburl','adsdec','tags','adimg','is_active')



