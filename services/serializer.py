# serializers.py

from rest_framework import serializers
from .models import ServicesList

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesList
        fields = '__all__'
