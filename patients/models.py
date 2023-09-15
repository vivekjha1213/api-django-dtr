from django.db import models

from Hospitals.models import Hospital


class Patient(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    medical_history = models.TextField()
    client = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
   
    


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
