from rest_framework import serializers
from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token

from .models import User


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField(allow_blank=True, allow_null=True)
    email = serializers.EmailField(allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'mobile', 'first_name', 'last_name')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'mobile': self.validated_data.get('referral_code', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.save()
        adapter.save_user(request, user, self)
        return user


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Token
        fields = ('key', 'user', 'username')

    def get_username(self, obj):
        return obj.user.username


class UserSerializer(serializers.ModelSerializer):
    """Serializes User instances"""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        )


class UserListSerializer(serializers.ModelSerializer):
    """Serializes User instances"""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        )
