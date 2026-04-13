# Backend/core/serializers.py
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'student')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError({
                "detail": "Username and password are required"
            })

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError({
                "detail": "Invalid username or password"
            })

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return {
            'username': user.username,
            'role': user.role,
            'user_id': user.id,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }