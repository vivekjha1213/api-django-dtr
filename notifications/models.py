from django.db import models
from Hospitals.models import Hospital

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('login', 'Login Notification'),
        ('doctor_addition', 'Doctor Addition Notification'),
        ('patient_addition', 'Patient Addition Notification'),
        ('appointment_booking', 'Appointment Booking Notification'),
    )

    recipient = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    updated_at = models.DateTimeField(auto_now=True)  
    message = models.TextField()

    def __str__(self):
        return self.message
