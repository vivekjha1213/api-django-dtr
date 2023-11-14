from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'notes', 'client')
    list_filter = ('client',)  
    search_fields = ('email', 'notes') 
    ordering = ('client',)  
