from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from decouple import config

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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


def handle_email(sender, recevier, subject, message):
    print("Handling email")
    # Set up SMTP connection
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = config("EMAIL_PORT")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recevier
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    # Send email
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(sender, recevier, msg.as_string())
