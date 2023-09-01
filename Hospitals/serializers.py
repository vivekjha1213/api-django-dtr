from rest_framework import serializers

import logging
from Hospitals.utils import Util
from .models import Hospital
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError
from .models import Hospital
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.urls import reverse


class HospitalRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Adding this field

    class Meta:
        model = Hospital
        fields = [
            "hospital_name",
            "owner_name",
            "profile_image",
            "user_logo",
            "city",
            "address",
            "email",
            "phone",
            "password",  # Include the password field here
            "user_type",
        ]

    def validate_email(self, email):
        if Hospital.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Hospital with this Email already exists."
            )
        return email

    def create(self, validated_data):
        password = validated_data.pop(
            "password"
        )  # Pop the password from validated_data

        hospital_manager = Hospital.objects.db_manager("default")
        hospital = hospital_manager.create_user(
            email=validated_data["email"],
            name=validated_data["hospital_name"],
            password=password,
            # Include other fields as needed
        )

        return hospital


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"


class HospitalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = [
            "hospital_name",
            "owner_name",
            "profile_image",
            "user_logo",
            "city",
            "address",
            "email",
            "phone",
            "password",
            "user_type",
        ]

    def validate(self, data):
        # Similar validation logic as above, check for uniqueness if required
        return data

    def update(self, instance, validated_data):
        # Update the password if provided
        password = validated_data.get("password")

        # Check if any data is being updated
        is_data_updated = False
        for field, value in validated_data.items():
            if getattr(instance, field) != value:
                is_data_updated = True
                break

        # Check if email and phone match the existing values
        email = validated_data.get("email")
        phone = validated_data.get("phone")
        existing_hospital = (
            Hospital.objects.filter(email=email, phone=phone)
            .exclude(pk=instance.pk)
            .first()
        )

        if existing_hospital:
            error_message = {
                "error": "Email or phone number already belongs to another hospital."
            }
            raise DRFValidationError(error_message)

        if password:
            validated_data["password"] = password

        if is_data_updated:
            return super().update(instance, validated_data)
        else:
            return instance  # No changes were made, return the existing instance


class HospitalLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Hospital
        fields = ["email", "password"]


# Password changed serilizer for 3 parameters old_pass,new_pass,confirm_pass.
class HospitalNewChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    new_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        user = self.context.get("user")

        if new_password != confirm_password:
            raise serializers.ValidationError(
                "New password and confirm password do not match"
            )

        if not user.check_password(old_password):
            raise serializers.ValidationError("Invalid old password")

        user.set_password(new_password)
        user.save()

        return attrs


# Password Reset email send url in Gmail..

""" 
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if Hospital.objects.filter(email=email).exists():
            user = Hospital.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.client_id))
           # print("Encoded UID", uid)
            token = PasswordResetTokenGenerator().make_token(user)
          #  print("Password Reset Token", token)
            link = "http://localhost:3000/api/user/reset/" + uid + "/" + token
            #print("Password Reset Link", link)
            # Send EMail
            body = "Click Following Link to Reset Your Password " + link
            data = {
                "subject": "Reset Your Password",
                "body": body,
                "to_email": user.email,
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("You are not a Registered User")





class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            hospital = Hospital.objects.get(email=email)
        except Hospital.DoesNotExist:
            raise serializers.ValidationError("You are not a Registered User")

        uid = urlsafe_base64_encode(force_bytes(hospital.client_id))
        token = PasswordResetTokenGenerator().make_token(hospital)
        reset_link = reverse("reset-password", kwargs={"uid": uid, "token": token})
        reset_url = self.context["request"].build_absolute_uri(reset_link)

        # Render HTML content using the template and hospital data
        context = {
            "owner_name": hospital.owner_name,
            "reset_url": reset_url,
        }
        html_content = render_to_string("password_reset_email.html", context)

        # Prepare data for sending email using Util class
        data = {
            "subject": "Reset Your Password",
            "body": html_content,
            "to_email": hospital.email,
        }

        # Use Util class to send email
        Util.send_email(data)

        return attrs


"""


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        
        try:
            hospital = Hospital.objects.get(email=email)
        except Hospital.DoesNotExist:
            raise serializers.ValidationError("You are not a Registered User")

        # Generate a unique identifier (uid) and password reset token (token)
        uid = urlsafe_base64_encode(force_bytes(hospital.client_id))
        token = PasswordResetTokenGenerator().make_token(hospital)

        # Create the reset link URL
        reset_url = f"http://localhost:3000/Hospital/reset/{uid}/{token}"

        # Render HTML content using the template and hospital data
        context = {
            "owner_name": hospital.owner_name,
            "reset_url": reset_url,
        }
        html_content = render_to_string("password_reset_email.html", context)

        # ------------->>>>>>   Include the reset URL and HTML content in the response data <<<<<<<<<<<<<<<-------------------------
        attrs["reset_url"] = reset_url
        attrs["html_content"] = html_content

        # Prepare data for sending email
        email_data = {
            "subject": "Reset Your Password",
            "body": html_content,
            "to_email": hospital.email,
        }

        # Use your email sending utility to send the email
        Util.send_email(email_data)

        return attrs




# Hospital PasswordReset Serializer............................................

class HospitalPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            password2 = attrs.get("password2")
            uid = self.context.get("uid")
            token = self.context.get("token")
            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match"
                )
            client_id = smart_str(urlsafe_base64_decode(uid))
            user = Hospital.objects.get(client_id=client_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not Valid or Expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is not Valid or Expired")
