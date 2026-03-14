from django.contrib import admin

from .models import ActivityLog, BatchJob, ImageUpload, Preset


@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "is_public", "uploaded_at")
    list_filter = ("is_public", "uploaded_at")
    search_fields = ("title", "user__username")


@admin.register(Preset)
class PresetAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "is_default", "created_at")
    list_filter = ("is_default",)


@admin.register(BatchJob)
class BatchJobAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "total_images", "processed_count", "status", "created_at")
    list_filter = ("status",)


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("user", "method", "path", "status_code", "timestamp")
    list_filter = ("method", "timestamp")
    search_fields = ("user__username", "path")
