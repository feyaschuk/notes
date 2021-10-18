from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from posts import views

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa

urlpatterns = [
    
    path("auth/", include("django.contrib.auth.urls")),
    path("misc/404", views.page_not_found),
    path("misc/500", views.server_error),
    path("", include("posts.urls")),
    path("admin/", admin.site.urls),
    
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)              

