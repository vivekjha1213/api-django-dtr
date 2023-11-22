from django.db import models
from apps.Hospitals.models import Hospital

CURRENT_PACKAGE_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    ]

class Package(models.Model):
    package_id =models.AutoField(primary_key=True,unique=True)
    package_name = models.CharField(max_length=200)
    client = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    current_package = models.CharField(
        max_length=10,  
        choices=CURRENT_PACKAGE_CHOICES,
        default='Monthly', 
    )
    description = models.TextField()
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    yearly_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.package_name
    
    
    class Meta:
        unique_together = ('package_name', 'client')

    
