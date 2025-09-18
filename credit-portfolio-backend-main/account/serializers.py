from django.contrib.auth.models import User
from rest_framework import serializers


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "is_staff", "is_superuser"]
        read_only_fields = ["username", "email", "is_staff", "is_superuser"]
