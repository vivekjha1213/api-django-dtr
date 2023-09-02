from django.db import models
from django.utils import timezone

class Feedback(models.Model):
    email = models.EmailField()
    notes = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback Email: {self.email}"


