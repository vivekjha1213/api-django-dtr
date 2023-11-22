from django.db import models
from apps.Hospitals.models import Hospital
from apps.Prescriptions.models import Prescription  # Assuming you have a Prescription model
from apps.Medicines.models import Medicine  # Assuming you have a Medicine model

class PrescriptionDetail(models.Model):
    prescription_detail_id = models.AutoField(primary_key=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=250)
    frequency = models.CharField(max_length=250)
    client = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    def __str__(self):
        return f"Prescription Detail {self.prescription_detail_id}"
