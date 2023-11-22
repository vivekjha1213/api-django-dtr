from django.contrib import admin

from apps.Hospitals.models import Hospital
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
        "client_id",
    )
    list_filter = ("department", "date_of_birth")  
    search_fields = ("first_name", "last_name", "email")
    ordering = ("-date_of_birth",) 
    search_fields = ['client__id', 'client__email']  # Search on both fields

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(client__id=search_term_as_int)
        except ValueError:
            queryset |= self.model.objects.filter(client__email__icontains=search_term)
        return queryset, use_distinct

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'client':
            kwargs['queryset'] = Hospital.objects.all().order_by('client_id')  
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def display_profile_image(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;">', obj.profile_image.url)
        else:
            return '-'
    display_profile_image.short_description = 'Profile Image'
