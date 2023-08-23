from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from rest_framework import status


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=["email","password","region","phone_number"]
        extra_kwargs = {"password": {"write_only": True}}

    def clean_data(self,data):
        email,password,region,phone_number=data["email"],data["password"],data["region"],data["phone_number"]
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(_("user with that email is already registered"))
        if CustomUser.objects.get(phone_number=phone_number).exists():
            raise serializers.ValidationError(_("farmer with the above phone number is registered try logging in"))
        return data
    
    def create(self,validated_data):
        password=validated_data["password"]
        user=CustomUser.objects.create(email=validated_data["email"],phone_number=validated_data["phone_number"],region=validated_data["region"])
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()


    
class ChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField()
    new_password=serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)