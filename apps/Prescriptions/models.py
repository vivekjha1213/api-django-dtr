from django.db import models
from apps.Hospitals.models import Hospital
from apps.patients.models import Patient  # Patient model
from apps.doctors.models import Doctor  #  Doctor model

class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    patient= models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor= models.ForeignKey(Doctor, on_delete=models.CASCADE)
    prescription_date_time = models. DateTimeField (null=True)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    


    def __str__(self):
        return f"Prescription {self.prescription_id} for Patient {self.patient}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)