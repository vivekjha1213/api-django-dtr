from django.db import models
from apps.Hospitals.models import Hospital
from apps.patients.models import Patient
from apps.doctors.models import Doctor


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Corrected field name and ForeignKey definition
    client= models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return f"Appointment ID: {self.appointment_id}"
