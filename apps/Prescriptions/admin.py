from django.contrib import admin
from .models import Prescription


if not admin.site.is_registered(Prescription):
    @admin.register(Prescription)
    class PrescriptionAdmin(admin.ModelAdmin):
        list_display = ('prescription_id', 'patient', 'doctor', 'prescription_date_time', 'created_at', 'updated_at', 'client')
        list_filter = ('prescription_date_time', 'created_at', 'updated_at')
        search_fields = ('patient__name', 'doctor__name')  


if not admin.site.is_registered(Prescription):
    admin.site.register(Prescription, PrescriptionAdmin)
