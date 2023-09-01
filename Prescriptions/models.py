from django.db import models
from Hospitals.models import Hospital
from patients.models import Patient  # Assuming you have a Patient model
from doctors.models import Doctor  # Assuming you have a Doctor model

class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    patient= models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor= models.ForeignKey(Doctor, on_delete=models.CASCADE)
    prescription_date = models.DateTimeField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    


    def __str__(self):
        return f"Prescription {self.prescription_id} for Patient {self.patient}"
