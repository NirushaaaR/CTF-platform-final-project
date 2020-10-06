from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from debug_toolbar import urls as debug_toolbar_urls
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += (
        [path("__debug__/", include(debug_toolbar_urls))]
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )
