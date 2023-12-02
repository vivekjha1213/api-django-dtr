from django.db import models
from apps.Hospitals.models import Hospital
from apps.patients.models import Patient  
from apps.doctors.models import Doctor  

class LabTest(models.Model):
    lab_test_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=250)
    test_date = models.DateField()
    results = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    client = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    


    def __str__(self):
        return f"LabTest {self.lab_test_id} for Patient {self.patient}"
