from django.contrib import admin
from .models import UploadedDataset

@admin.register(UploadedDataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at', 'row_count')
    readonly_fields = ('uploaded_at', 'summary')
