from django.contrib import admin
from .models import Bed

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "get_department_name",  
        "is_occupied",
    )
    list_filter = ("is_occupied",)  
    search_fields = ("client__name",) 
    ordering = ("client",) 

    def get_department_name(self, obj):
        return obj.department.name if obj.department else "-"  
    get_department_name.short_description = 'Department' 
