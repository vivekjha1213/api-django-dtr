from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "gender",
        "email",
        "contact_number",
        "address",
        "date_of_birth",
        "medical_history",
        "client",
    )
    list_filter = ("gender",)  
    search_fields = ("first_name", "last_name", "email")
    ordering = ("-date_of_birth",) 
