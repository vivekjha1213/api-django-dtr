# tasks.py

import time  
from django.core.mail import EmailMessage
from settings.celery import shared_task

@shared_task
def send_email_with_delay(subject, body, from_email, to_email, delay_seconds=1):
    # Sleep for the specified number of seconds (e.g., 1 second)
    time.sleep(1)

    # Send the email
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[to_email],
    )
    email.content_subtype = "html"  # 
    email.send()
