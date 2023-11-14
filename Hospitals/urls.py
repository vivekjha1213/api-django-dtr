from django.urls import path

from Hospitals import api


# from .views import (
#     DeatilsHospitalView,
#     DepartmentNurseDataJoinView,
#     HospitalChangePasswordView,
#     HospitalDataJoinView,
#     HospitalDeleteView,
#     HospitalListAPIView,
#     HospitalLoginView,
#     HospitalLogoutAPIView,
#     HospitalPasswordResetView,
#     HospitalRegistrationView,
#     HospitalRetrieveAPIView,
#     HospitalUpdateView,
#     MedicinesHospitalDataJoinView,
#     PrescriptionDataJoinView,
#     PrescriptionDetailPrescriptionsJoinHospital,
#     SendOTPView,
#     SendPasswordResetEmailView,
#     TotalHospitalView,
#     VerifyOTPView,
    
# )

PREFIX ='hospital'
urlpatterns = [
    path(f"{PREFIX}/add", api.HospitalRegistrationView.as_view(), name="register"),
    path(f"{PREFIX}/list", api.HospitalListAPIView.as_view(), name="hospital-list"),
    path(f"{PREFIX}/list/<str:client_id>", api.HospitalRetrieveAPIView.as_view(), name="list-By-id"),
    path(f"{PREFIX}/update/<str:client_id>", api.HospitalUpdateView.as_view(), name="hospital-update"),
    path(f"{PREFIX}/delete/<str:client_id>",api. HospitalDeleteView.as_view(), name="hospital-retrieve-delete"),
    path(f"{PREFIX}/total", api.TotalHospitalView.as_view(), name="hospital-retrieve-total"),
    path(f"{PREFIX}/login", api.HospitalLoginView.as_view(), name="Login"),
    path(f"{PREFIX}/logout", api.HospitalLogoutAPIView.as_view(), name="hospital-logout"),
    path(f"{PREFIX}/change-password",api. HospitalChangePasswordView.as_view(), name="change-password"),
    path(f"{PREFIX}/send-reset-password-email", api.SendPasswordResetEmailView.as_view(), name="send-reset-password-email"),
    path(f"{PREFIX}/reset-password/<uid>/<token>",api.HospitalPasswordResetView.as_view(), name="reset-password"),
    path(f"{PREFIX}/hospitals-doctorts-patients", api.DeatilsHospitalView.as_view(), name="Doctor_With-Hospital"),
    path(f"{PREFIX}/hospitals-details-all", api.HospitalDataJoinView.as_view(), name="Doctor_With-Hospital"),
    path(f"{PREFIX}/Nurse-department-all", api.DepartmentNurseDataJoinView.as_view(), name="Nurse_With-Hospital"),
    path(f"{PREFIX}/medicines-hospital-all", api.MedicinesHospitalDataJoinView.as_view(), name="medicines-hospital-all"),
    path(f"{PREFIX}/prescription-hospital-all", api.PrescriptionDataJoinView.as_view(), name="prescription-hospital-all"),
    path(f"{PREFIX}/prescriptionDetail-Hospital-all",api.PrescriptionDetailPrescriptionsJoinHospital.as_view(), name="PrescriptionDetail-hospital-all"),
    path(f"{PREFIX}/send-otp", api.SendOTPView.as_view(), name="send_otp"),
    path(f"{PREFIX}/verify-otp", api.VerifyOTPView.as_view(), name="verify_otp"),
]