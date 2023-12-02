from django.db import models
from django.utils import timezone
from apps.Hospitals.models import Hospital

class Feedback(models.Model):
    client = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    email = models.EmailField()
    notes = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Feedback from {self.email} at {self.created_at}"
