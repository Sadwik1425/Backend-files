from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Region, Indication, SavedProtocol, ProtocolRequest

User = get_user_model()

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']

class IndicationSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)

    class Meta:
        model = Indication
        fields = ['id', 'region', 'region_name', 'name']

class ProtocolSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = SavedProtocol
        fields = '__all__'

class ProtocolRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = ProtocolRequest
        fields = '__all__'
