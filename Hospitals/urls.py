from django.urls import path


from .views import (
    DeatilsHospitalView,
    DepartmentNurseDataJoinView,
    HospitalChangePasswordView,
    HospitalDataJoinView,
    HospitalDeleteView,
    HospitalListAPIView,
    HospitalLoginView,
    HospitalLogoutAPIView,
    HospitalPasswordResetView,
    HospitalRegistrationView,
    HospitalRetrieveAPIView,
    HospitalUpdateView,
    MedicinesHospitalDataJoinView,
    PrescriptionDataJoinView,
    PrescriptionDetailPrescriptionsJoinHospital,
    SendOTPView,
    SendPasswordResetEmailView,
    TotalHospitalView,
    VerifyOTPView,
    
)

PREFIX ='hospital'
urlpatterns = [
    path(f"{PREFIX}/add", HospitalRegistrationView.as_view(), name="register"),
    path(f"{PREFIX}/list", HospitalListAPIView.as_view(), name="hospital-list"),
    path(f"{PREFIX}/list/<str:client_id>", HospitalRetrieveAPIView.as_view(), name="list-By-id"),
    path(f"{PREFIX}/update/<str:client_id>", HospitalUpdateView.as_view(), name="hospital-update"),
    path(f"{PREFIX}/delete/<str:client_id>", HospitalDeleteView.as_view(), name="hospital-retrieve-delete"),
    path(f"{PREFIX}/total", TotalHospitalView.as_view(), name="hospital-retrieve-total"),
    path(f"{PREFIX}/login", HospitalLoginView.as_view(), name="Login"),
    path(f"{PREFIX}/logout", HospitalLogoutAPIView.as_view(), name="hospital-logout"),
    path(f"{PREFIX}/change-password", HospitalChangePasswordView.as_view(), name="change-password"),
    path(f"{PREFIX}/send-reset-password-email", SendPasswordResetEmailView.as_view(), name="send-reset-password-email"),
    path(f"{PREFIX}/reset-password/<uid>/<token>", HospitalPasswordResetView.as_view(), name="reset-password"),
    path(f"{PREFIX}/hospitals-doctorts-patients", DeatilsHospitalView.as_view(), name="Doctor_With-Hospital"),
    path(f"{PREFIX}/hospitals-details-all", HospitalDataJoinView.as_view(), name="Doctor_With-Hospital"),
    path(f"{PREFIX}/Nurse-department-all", DepartmentNurseDataJoinView.as_view(), name="Nurse_With-Hospital"),
    path(f"{PREFIX}/medicines-hospital-all", MedicinesHospitalDataJoinView.as_view(), name="medicines-hospital-all"),
    path(f"{PREFIX}/prescription-hospital-all", PrescriptionDataJoinView.as_view(), name="prescription-hospital-all"),
    path(f"{PREFIX}/prescriptionDetail-Hospital-all", PrescriptionDetailPrescriptionsJoinHospital.as_view(), name="PrescriptionDetail-hospital-all"),
    path(f"{PREFIX}/send-otp", SendOTPView.as_view(), name="send_otp"),
    path(f"{PREFIX}/verify-otp", VerifyOTPView.as_view(), name="verify_otp"),
]