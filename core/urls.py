from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework.permissions import IsAuthenticated
from apps.Hospitals.permissions import UnrestrictedPermission
from apps.Hospitals.api import index  
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Orionqo",
        default_version="v1.o",
        description="Stage Restservice",
        terms_of_service="Orionqo TM",
        contact=openapi.Contact(email="support@orionqo.com"),
        license=openapi.License(name="orionqo.com"),
    ),
    public=True,
    permission_classes=[UnrestrictedPermission]
)


#DRF
urlpatterns = [
    re_path(
        r"^doc(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("", index, name="index"),  
    path("admin/", admin.site.urls),
    
    
    #DRF API
    path("api/", include("apps.Hospitals.urls")),
    path("api/", include("apps.patients.urls")),
    path("api/", include("apps.doctors.urls")),
    path("api/", include("apps.Departments.urls")),
    path("api/", include("apps.Nurses.urls")),
    path("api/", include("apps.Medicines.urls")),
    path("api/", include("apps.Appointments.urls")),
    path("api/", include("apps.Beds.urls")),
    path("api/", include("apps.Prescriptions.urls")),
    path("api/", include("apps.PrescriptionDetails.urls")),
    path("api/", include("apps.Invoices.urls")),
    path("api/", include("apps.Payments.urls")),
    path("api/", include("apps.LabTests.urls")),
    path("api/", include("apps.feedbacks.urls")),
    path("api/", include("apps.packages.urls")),
    
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
