from django.contrib import admin
from django.urls import path, include
from accounts.views import register
from django.conf import settings
from django.conf.urls.static import static


# (Optional) keep Django’s default error handlers
handler400 = 'django.views.defaults.bad_request'
handler403 = 'django.views.defaults.permission_denied'
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("services.urls")),              # NO namespace here
    path("bookings/", include("bookings.urls")),     # NO namespace here
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", register, name="register"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")