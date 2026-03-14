import os

from django.conf import settings

from .models import BatchJob, ImageUpload
from .halftone import apply_halftone


def process_batch(batch_id):
    """Process all images in a batch job."""
    batch = BatchJob.objects.get(pk=batch_id)
    batch.status = "processing"
    batch.save(update_fields=["status"])

    images = ImageUpload.objects.filter(batch=batch)
    had_failures = False
    for upload in images:
        try:
            original_path = upload.original.path
            filename = f"halftone_{upload.pk}.png"
            output_path = os.path.join(settings.MEDIA_ROOT, "processed", filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            apply_halftone(original_path, output_path)

            upload.processed = f"processed/{filename}"
            upload.save(update_fields=["processed"])

            batch.processed_count += 1
            batch.save(update_fields=["processed_count"])
        except Exception:
            had_failures = True
            continue

    batch.status = "failed" if had_failures else "completed"
    batch.save(update_fields=["status"])
