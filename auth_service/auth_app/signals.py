from django.db.models.signals import post_save, Signal
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CustomUser
from decouple import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

send_mail = Signal()


@receiver(send_mail)
def handle_otp_email(sender, recevier, **kwargs):
    # Set up SMTP connection
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = config("EMAIL_PORT")

    # Compose email message
    sender_email = "your_email@example.com"
    receiver_email = recevier
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
