from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "appointment_id",
        "patient",
        "doctor",
        "appointment_date",
        "start_time",
        "end_time",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("doctor", "appointment_date", "status")
    search_fields = ("patient__full_name", "doctor__full_name", "appointment_date")
    ordering = ("-appointment_date", "start_time")
