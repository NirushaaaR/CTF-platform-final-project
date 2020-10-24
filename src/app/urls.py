from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("core.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    from debug_toolbar import urls as debug_toolbar_urls

    urlpatterns += [path("__debug__/", include(debug_toolbar_urls))]
