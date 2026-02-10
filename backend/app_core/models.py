from django.db import models

# stores each csv upload with its computed summary
class UploadedDataset(models.Model):
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    csv_file = models.FileField(upload_to='datasets/')
    summary = models.JSONField(default=dict, blank=True)
    row_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.name} ({self.uploaded_at:%Y-%m-%d})"
