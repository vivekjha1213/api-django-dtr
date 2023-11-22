from django.db import models

from apps.Hospitals.models import Hospital

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    client= models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['department_name', 'client']

    def __str__(self):
        return self.department_name
