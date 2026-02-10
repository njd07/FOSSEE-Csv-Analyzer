from .models import UploadedDataset

MAX_HISTORY = 5

# delete old uploads, keep only 5
def cleanup_old_datasets():
    all_ds = UploadedDataset.objects.order_by('-uploaded_at')
    if all_ds.count() > MAX_HISTORY:
        keep_ids = list(all_ds[:MAX_HISTORY].values_list('id', flat=True))
        UploadedDataset.objects.exclude(id__in=keep_ids).delete()
