from django.contrib import admin
from .models import Package

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "package_name",
        "client",
        "current_package",
        "description",
        "monthly_price",
        "yearly_price",
        "start_date",
        "end_date",
    )
    list_filter = ("client",) 
    search_fields = ("package_name", "description", "client__name") 
    ordering = ("-start_date",) 
