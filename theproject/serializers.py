from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = client
        fields = '__all__'
