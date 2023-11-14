from django.contrib import admin
from .models import Doctor
from django.utils.html import format_html

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "display_profile_image", 
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

    def display_profile_image(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;">', obj.profile_image.url)
        else:
            return '-'
    display_profile_image.short_description = 'Profile Image'
