from django.db import models
from Departments.models import Department
from Hospitals.models import Hospital


class Doctor(models.Model):
    SPECIALTY_CHOICES = [
        ("Cardiology", "Cardiology"),
        ("Dermatology", "Dermatology"),
        ("Neurology", "Neurology"),
        ("Orthopedics", "Orthopedics"),
        ("Pediatrics", "Pediatrics"),
        ("Ophthalmology", "Ophthalmology"),
        ("Gynecology", "Gynecology"),
        ("Urology", "Urology"),
        ("Oncology", "Oncology"),
        ("Psychiatry", "Psychiatry"),
        ("ENT", "ENT"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    doctor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True)
    specialty = models.CharField(max_length=255, choices=SPECIALTY_CHOICES)
    qualifications = models.TextField()
    address = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="doctor_profile/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    client = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
