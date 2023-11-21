from django.contrib import admin
from .models import Package
from django import forms


class PackageAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['client'].widget.can_add_related = True

    class Meta:
        model = Package
        fields = '__all__'

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "package_name",
        "client_id",
        "current_package",
        "description",
        "monthly_price",
        "yearly_price",
        "start_date",
        "end_date",
    )
    list_filter = ("client_id",) 
    search_fields = ("package_name", "description", "client__name") 
    ordering = ("-start_date",) 
    form = PackageAdminForm  
