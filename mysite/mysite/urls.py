from django.contrib import admin
from django.urls import path, include
from mysite import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authViews

urlpatterns = [
    path("", views.index, name="index"),
    path('admin/', admin.site.urls),
    path("center/", include("center.urls", namespace="center")),
    path("vaccine/", include("vaccine.urls", namespace="vaccine")),
    path("campaign/", include("campaign.urls", namespace = "campaign")),
    path("accounts/", include("user.urls", namespace="user")),
    path("vaccination/", include("vaccination.urls", namespace="vaccination")),

    path("password_reset/", authViews.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        authViews.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        authViews.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        authViews.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


admin.site.site_header = "Book My Vaccine"
admin.site.site_title = "Book My Vaccine"
admin.site.index_title = "Admin Panel"
