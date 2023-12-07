from django.contrib import admin
from .models import Medicine


if not admin.site.is_registered(Medicine):
    @admin.register(Medicine)
    class MedicineAdmin(admin.ModelAdmin):
        list_display = ('medicine_id', 'medicine_name', 'manufacturer', 'unit_price', 'stock_quantity', 'created_at', 'updated_at', 'client')
        list_filter = ('manufacturer', 'client')
        search_fields = ('medicine_name', 'manufacturer')  


if not admin.site.is_registered(Medicine):
    admin.site.register(Medicine, MedicineAdmin)
