from django.db import models
from apps.Hospitals.models import Hospital
from apps.patients.models import Patient  

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    invoice_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Adjust max_digits and decimal_places as needed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Hospital, on_delete=models.CASCADE)
  


    def __str__(self):
        return f"Invoice {self.invoice_id} for Patient {self.patient}"
