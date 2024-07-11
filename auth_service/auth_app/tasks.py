from celery import shared_task
from django.db.models import Sum
from decimal import Decimal
from .signals import send_mail


@shared_task
def send_otp_email(recevier, otp):

    print(f"Sending email to {recevier} with message: {otp}")
    send_mail.send(sender=None, recevier=recevier, otp=otp)  # add task to send email
