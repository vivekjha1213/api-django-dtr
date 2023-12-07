from django.contrib import admin
from .models import PrescriptionDetail


if not admin.site.is_registered(PrescriptionDetail):
    @admin.register(PrescriptionDetail)
    class PrescriptionDetailAdmin(admin.ModelAdmin):
        list_display = ('prescription_detail_id', 'prescription', 'medicine', 'dosage', 'frequency', 'client')
        list_filter = ('prescription__prescription_date_time', 'client')
        search_fields = ('prescription__patient__name', 'medicine__name') 


if not admin.site.is_registered(PrescriptionDetail):
    admin.site.register(PrescriptionDetail, PrescriptionDetailAdmin)
