from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name", "last_name",  "username", "email", "password"]

    def create(self, validated_data: dict):
        user = User(
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            username = validated_data["username"],
            email = validated_data["email"]
        )
        user.set_password(validated_data['password'])
        user.save()
        return super().create(validated_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "password"]


