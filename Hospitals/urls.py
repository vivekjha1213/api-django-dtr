from django.urls import path


from Hospitals.views import (
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
    SendPasswordResetEmailView,
    TotalHospitalView,
)

urlpatterns = [
    path("add/", HospitalRegistrationView.as_view(), name="register"),
    path("list/", HospitalListAPIView.as_view(), name="hospital-list"),
    path(
        "list/<str:client_id>/",
        HospitalRetrieveAPIView.as_view(),
        name="list-By-id",
    ),
    path(
        "update/<str:client_id>/",
        HospitalUpdateView.as_view(),
        name="hospital-update",
    ),
    path(
        "delete/<str:client_id>/",
        HospitalDeleteView.as_view(),
        name="hospital-retrieve-delete",
    ),
    path(
        "total/",
        TotalHospitalView.as_view(),
        name="hospital-retrieve-total",
    ),
    path("login/", HospitalLoginView.as_view(), name="Login"),
    path("logout/", HospitalLogoutAPIView.as_view(), name="hospital-logout"),
     path(
         "change-password/", HospitalChangePasswordView.as_view(), name="change-password"
     ),
     path(
        "send-reset-password-email/",
        SendPasswordResetEmailView.as_view(),
        name="send-reset-password-email",
    ),
     path(
         "reset-password/<uid>/<token>/",
         HospitalPasswordResetView.as_view(),
         name="reset-password",
     ),
       path(
        "hospitals-doctorts-patients/", DeatilsHospitalView.as_view(), name="Doctor_With-Hospital"
    ),
       
          path(
        "hospitals-details-all/", HospitalDataJoinView.as_view(), name="Doctor_With-Hospital"
    ),
          
                 path(
        "Nurse-department-all/", DepartmentNurseDataJoinView.as_view(), name="Nurse_With-Hospital"
    ),
    
    
    
    
    
    
]
