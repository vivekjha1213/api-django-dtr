from django.db import models
from apps.Departments.models import Department
from apps.Hospitals.models import Hospital
from apps.patients.models import Patient


class Bed(models.Model):
    bed_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=10, unique=True)
    is_occupied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)

    def generate_bed_number(self):
        last_bed = Bed.objects.order_by("-bed_id").first()

        if last_bed is None:
            return "BDN00001"

        last_number = (
            int(last_bed.bed_number[3:]) if last_bed.bed_number[3:].isdigit() else 0
        )
        new_number = last_number + 1
        return f"BDN{new_number:05d}"

    def save(self, *args, **kwargs):
        if not self.bed_number:
            self.bed_number = self.generate_bed_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bed {self.bed_number} in Department {self.department} at {self.client}"
