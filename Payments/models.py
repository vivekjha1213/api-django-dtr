from django.db import models
from Hospitals.models import Hospital
from Invoices.models import Invoice  # Assuming you have an Invoice model

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Adjust max_digits and decimal_places as needed

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    client = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    

    def __str__(self):
        return f"Payment {self.payment_id} for Invoice {self.invoice}"
