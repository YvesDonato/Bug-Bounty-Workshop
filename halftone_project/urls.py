from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# URL registration order matters — processor URLs use an empty prefix ("") and will
# shadow any pattern registered after them. accounts/ must be declared first.
# Swapping the order causes login/logout to 404 silently in some Django versions.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("processor.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
