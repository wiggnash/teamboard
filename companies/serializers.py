from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    company_name = serializers.CharField()
    email = serializers.EmailField()

    def validate_username(self, value):
        username_taken = User.objects.filter(username=value).exists()

        if username_taken:
            raise serializers.ValidationError("This username is already taken! Please try again.")
        
        return value
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
