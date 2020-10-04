from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from debug_toolbar import urls as debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include(debug_toolbar_urls))]
