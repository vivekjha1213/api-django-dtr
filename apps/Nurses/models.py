from django.db import models
from apps.Departments.models import Department

from apps.Hospitals.models import Hospital


class Nurse(models.Model):
    nurse_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    client = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    class Meta:
        unique_together = ['first_name', 'last_name', 'date_of_birth']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
