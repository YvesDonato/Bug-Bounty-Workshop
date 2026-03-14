from django.urls import path

from . import views

urlpatterns = [
    path("", views.upload_view, name="upload"),
    path("result/<int:pk>/", views.result_view, name="result"),
    path("gallery/", views.gallery_view, name="gallery"),
    path("shared/<str:token>/", views.shared_view, name="shared"),
    path("presets/", views.preset_list_view, name="preset_list"),
    path("presets/create/", views.preset_create_view, name="preset_create"),
    path("presets/import/", views.preset_import_view, name="preset_import"),
    path("batch/", views.batch_upload_view, name="batch_upload"),
    path("batch/<int:batch_id>/status/", views.batch_status_view, name="batch_status"),
]
