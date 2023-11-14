from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "profile_image",
        "gender",
        "email",
        "contact_number",
        "date_of_birth",
        "specialty",
        "qualifications",
        "address",
        "department",
        "client",
    )
    list_filter = ("department", "date_of_birth")  
    search_fields = ("first_name", "last_name", "email")
    ordering = ("-date_of_birth",) 
