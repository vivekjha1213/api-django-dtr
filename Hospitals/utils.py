# Hospitals/utils.py
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import os

from rest_framework_simplejwt.settings import api_settings


def custom_payload_handler(user):
    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    payload[
        "client_id"
    ] = user.client_id  # Assuming client_id is your primary key field
    return payload


# send email by using EmailMessage Class..

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email=os.environ.get("EMAIL_FROM"),
            to=[data["to_email"]],
            
            
        )
        email.content_subtype = "html"  # Set content type to HTML
        email.send()


    @staticmethod
    def send_welcome_email(hospital):
        subject = "Welcome to Our Platform"
        from_email = os.environ.get("EMAIL_FROM")  # Use the sender email address from environment
        to_email = hospital.email
        product_name="dtroffle"
        context = {
            "owner_name": hospital.owner_name,
            "product_name":product_name
        }
        html_content = render_to_string("welcome_email_template.html", context)
        data = {
            "subject": subject,
            "body": html_content,
            "to_email": to_email,
            "from_email": from_email,  # Pass the sender email to the send_email method
        }
        Util.send_email(data)
        
        
        
        
              
    @staticmethod
    def send_password_change_email(hospital):
         subject = "Password Changed Successfully"
         from_email = os.environ.get("EMAIL_FROM")  # Use the sender email address from environment
         to_email = hospital.email
         product_name = "dtroffle"  # Replace with your product name
         
         context = {
        "owner_name": hospital.owner_name,  # Use the correct attribute for hospital owner's name
        "product_name": product_name,
    }
         html_content = render_to_string("password_changed_template.html", context)
         data = {
        "subject": subject,
        "body": html_content,
        "to_email": to_email,
        "from_email": from_email,  # Pass the sender email to the send_email method
    }
         Util.send_email(data)

        
      
      
        
   
   