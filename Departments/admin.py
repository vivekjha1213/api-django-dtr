from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "department_name",
    )
    list_filter = ("department_name",)  
    search_fields = ("client", "department_name") 
    ordering = ("department_name",)  
