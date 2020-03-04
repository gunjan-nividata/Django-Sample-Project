from rest_framework import serializers

from django.contrib.auth.models import Permission
from .models import User
from rest_auth.models import TokenModel


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    """
    TokenSerializer which returns token and user_id.
    """
    class Meta:
        model = TokenModel
        fields = ('key', 'user')


class UserInfoSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(source="user_permissions", many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined',
                  'objects', 'is_superuser', 'groups', 'permissions']
