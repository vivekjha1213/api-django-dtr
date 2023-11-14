from django.contrib import admin
from django.utils.html import format_html
from .models import Hospital

admin.sites.AdminSite.site_header = 'Orionqo DashBoard'
admin.sites.AdminSite.site_title = 'Orionqo.com'
admin.sites.AdminSite.index_title = 'Orionqo.com'


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = (
        "hospital_name",
        "owner_name",
        "display_profile_image",
        "display_user_logo",
        "city",
        "address",
        "email",
        "phone", 
        "user_type"
    )
    list_filter = ('city',)  
    search_fields = ('email', 'owner_name') 
    ordering = ('hospital_name',)  

    fieldsets = (
        (None, {
            'fields': ('hospital_name', 'owner_name', 'city', 'address', 'email', 'phone')
        }),
        ('Additional Information', {
            'fields': ('user_logo', 'password', 'user_type'),
            'classes': ('collapse',) 
        }),
    )

    def display_profile_image(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;">', obj.profile_image.url)
        else:
            return '-'
    display_profile_image.short_description = 'Profile Image'

    def display_user_logo(self, obj):
        if obj.user_logo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;">', obj.user_logo.url)
        else:
            return '-'
    display_user_logo.short_description = 'User Logo'


