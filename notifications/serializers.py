from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("recipient_id", "timestamp", "notification_type", "message")

    def to_representation(self, instance):
        if instance.notification_type == "appointment_booking":
            instance.message = f"Appointment booked: {instance.message}"
        elif instance.notification_type == "doctor_addition":
            instance.message = f"Doctor added: {instance.message}"
        elif instance.notification_type == "patient_addition":
            instance.message = f"Patient added: {instance.message}"
        elif instance.notification_type == "login":
            instance.message = f"Login: {instance.message}"
        return super().to_representation(instance)
