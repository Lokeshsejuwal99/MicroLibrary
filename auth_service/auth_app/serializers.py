from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "password",
            "password_confirmation",
            "is_active",
            "is_staff",
            "twofa_enabled",
        )

    def validate(self, data):
        # Check that the password and password_confirmation match
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": "Passwords do not match"}
            )
        return data

    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data.pop("password_confirmation", None)
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(CustomUserSerializer, self).create(validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    msg = "User account is disabled."
                    raise serializers.ValidationError(msg)
            else:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg)
        else:
            msg = "Must include 'email' and 'password'."
            raise serializers.ValidationError(msg)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        print(user.twofa_enabled)
        response = {
            "access_token": access_token,
            "refresh_token": str(refresh),
            "user_id": user.id,
            "2fa": user.twofa_enabled,
            "email": user.email,
        }
        print(response)

        return response
