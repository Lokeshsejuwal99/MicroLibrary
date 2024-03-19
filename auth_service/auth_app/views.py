from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config


class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "User created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if serializer.validated_data["2fa"] == True:
                # Send 2FA code to user
                print("Sending 2FA code to user")
                # integrate mailtrap to send 2FA code to user
                # Send 2FA code to user
                print("Sending 2FA code to user")

                # Set up SMTP connection
                EMAIL_HOST = config("EMAIL_HOST")
                EMAIL_HOST_USER = config("EMAIL_HOST_USER")
                EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
                EMAIL_PORT = config("EMAIL_PORT")

                # Compose email message
                sender_email = "your_email@example.com"
                receiver_email = serializer.validated_data["email"]
                subject = "2FA Code"
                message = "Your 2FA code is: 123456"  # Replace with actual 2FA code

                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = receiver_email
                msg["Subject"] = subject
                msg.attach(MIMEText(message, "plain"))

                # Send email
                with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                    server.sendmail(sender_email, receiver_email, msg.as_string())
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]

            # Set cookies for access and refresh tokens
            response = Response(
                {
                    "success": True,
                    "message": "User Logged in successfully",
                    "data": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)

            return response

        except Exception as e:
            return Response(
                {"success": False, "error": "An error occurred during login."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
