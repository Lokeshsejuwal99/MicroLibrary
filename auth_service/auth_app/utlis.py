from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import random


def generate_otp():
    # Generate a random 6-digit OTP
    otp = random.randint(100000, 999999)
    return otp


if __name__ == "__main__":
    otp = generate_otp()
    print(f"Generated OTP: {otp}")


def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return access_token, refresh_token
