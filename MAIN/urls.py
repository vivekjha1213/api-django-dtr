from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework.permissions import IsAuthenticated
from Hospitals.views import index  # Import your index view

# drf_yasg code starts here
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Hospital Management System API",
        default_version="v1",
        description="This API is only for Testing..",
        terms_of_service="Hms",
        contact=openapi.Contact(email="vivek.jha@dtroffle.com"),
        license=openapi.License(name="RestFul API's"),
    ),
    public=True,
    permission_classes=(IsAuthenticated,),  # Require authentication to access
)


# ... rest of your code ...
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
    path("", index, name="index"),  # Add this line for the root URL
    path("platform/", admin.site.urls),
    path("Hospital/", include("Hospitals.urls")),
    path("Patient/", include("patients.urls")),
    path("Doctor/", include("doctors.urls")),
    path("Department/", include("Departments.urls")),
    path("Nurse/", include("Nurses.urls")),
    path("Medicine/", include("Medicines.urls")),
    path("Appointment/", include("Appointments.urls")),
    path("Bed/", include("Beds.urls")),
    path("Prescription/", include("Prescriptions.urls")),
    path("PrescriptionDetail/", include("PrescriptionDetails.urls")),
    path("Invoice/", include("Invoices.urls")),
    path("Payment/", include("Payments.urls")),
    path("LabTest/", include("LabTests.urls")),
    path("Feedback/", include("feedbacks.urls")),
    path("notification/", include("notifications.urls")),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
