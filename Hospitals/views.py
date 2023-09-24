from importlib.abc import PathEntryFinder
import logging

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from Hospitals.permissions import UnrestrictedPermission
from Hospitals.utils import Util
from django.db.models import F
from django.db.models import CharField, Value

from django.utils import timezone
from Nurses.models import Nurse

from doctors.models import Doctor  # Import timezone from django.utils


from patients.models import Patient

from .models import Hospital
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate  # Import the authenticate function
from django.contrib.auth import logout  # for logout
from django.shortcuts import render


from .models import Hospital
from .serializers import (
    HospitalLoginSerializer,
    HospitalNewChangePasswordSerializer,
    HospitalPasswordResetSerializer,
    HospitalRegisterSerializer,
    HospitalSerializer,
    HospitalUpdateSerializer,
    SendPasswordResetEmailSerializer,
)


logger = logging.getLogger("Hospitals.Hospital")


# Create your views here.
def index(request):
    logger.info("Accessing the index view.")
    return render(request, "index.html")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class HospitalRegistrationView(APIView):
    def post(self, request):
        serializer = HospitalRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Hospital Added successfully."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class HospitalUpdateView(UpdateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalUpdateSerializer
    lookup_field = "client_id"  # Replace with the actual lookup field

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {"message": "Hospital updated successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class HospitalDeleteView(APIView):
    def delete(self, request, client_id, format=None):
        try:
            hospital = Hospital.objects.get(client_id=client_id)
        except Hospital.DoesNotExist:
            return Response(
                {"error": "Hospital not found."}, status=status.HTTP_404_NOT_FOUND
            )

        hospital.delete()
        return Response(
            {"message": "Hospital deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class HospitalListAPIView(generics.ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class HospitalRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]  # Requires authentication
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    lookup_field = "client_id"


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class TotalHospitalView(APIView):
    def get(self, request, format=None):
        total_hospitals = Hospital.objects.count()
        return Response({"total_hospitals": total_hospitals}, status=status.HTTP_200_OK)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# login api
class HospitalLoginView(APIView):
    permission_classes = [UnrestrictedPermission]

    def post(self, request):
        serializer = HospitalLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # Authenticate the user
        hospital = authenticate(email=email, password=password)

        if hospital is not None:
            # Manually update the last_login field
            hospital.last_login = (
                timezone.now()
            )  # Import timezone if not already imported
            hospital.save()  # Save the user instance to update last_login

            # Generate tokens
            refresh = RefreshToken.for_user(hospital)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Include client_id and is_admin in the response
            client_id = hospital.client_id
            is_admin = hospital.is_admin
            user_type = hospital.user_type

            # Save tokens to the hospital instance and then save the instance
            hospital.access_token = access_token
            hospital.refresh_token = refresh_token
            hospital.save()

            Util.send_welcome_email(hospital)  # Call send_welcome_email here

            return Response(
                {
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "client_id": client_id,
                    "is_admin": is_admin,  # Include the is_admin flag
                    "user_type": user_type,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid email or password. Please check your credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# logout api.....
class HospitalLogoutAPIView(APIView):
    def delete(self, request, format=None):
        logger.info("Logout requested for user")
        if request.user.is_authenticated:
            logger.info("Logout requested for user")
            logout(request)  # Logout the user
        return Response({"message": "Logout success"}, status=status.HTTP_200_OK)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class HospitalChangePasswordView(APIView):
    def post(self, request, format=None):
        serializer = HospitalNewChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)

        # Send password change success email
        Util.send_password_change_email(request.user)
        return Response(
            {"message": "Password Changed Successfully"}, status=status.HTTP_200_OK
        )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# @email @Post api for send reset link in front end view ....
class SendPasswordResetEmailView(APIView):
    permission_classes = [UnrestrictedPermission]

    def post(self, request, format=None):
        logger.info("Password reset email requested")

        # Create the serializer instance with the 'request' object in the context
        serializer = SendPasswordResetEmailSerializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Password Reset link sent. Please check your Email"},
            status=status.HTTP_200_OK,
        )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# @email for change password redirect
class HospitalPasswordResetView(APIView):
    def post(self, request, uid, token, format=None):
        logger.info("Password reset requested for user with UID: %s", uid)
        serializer = HospitalPasswordResetSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Password Reset Successfully"}, status=status.HTTP_200_OK
        )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class DeatilsHospitalView(generics.ListAPIView):
    serializer_class = None

    def get_queryset(self):
        hospital = Hospital.objects.values(
            "client_id",
            "hospital_name",
            "name",
            "owner_name",
            "city",
            "address",
            "email",
            "phone",
            "password",
            "user_type",
            "profile_image",
            "user_logo",
            "last_login",
            "created_at",
            "updated_at",
            "is_active",
        ).first()  # Assuming there's only one hospital

        # Query the Doctor model for one doctor
        doctor = Doctor.objects.values(
            "client_id",
            "first_name",
            "last_name",
            "profile_image",
            "gender",
            "email",
            "contact_number",
            "date_of_birth",
            "specialty",
            "qualifications",
            "address",
            "department",
        ).first()

        # Query the Patient model for one patient
        patient = Patient.objects.values(
            "client_id",
            "first_name",
            "last_name",
            "gender",
            "email",
            "contact_number",
            "address",
            "date_of_birth",
            "medical_history",
        ).first()

        # Create a dictionary to hold the data
        combined_data = {
            "hospital": hospital,
            "doctor": doctor,
            "patient": patient,
        }

        return [combined_data]  # Return as a list of dictionaries

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)


class HospitalDataJoinView(generics.ListAPIView):
    serializer_class = None

    def get_queryset(self):
        # Query the Hospital model and join with Doctor and Patient models
        queryset = (
            Hospital.objects.annotate(
                doctor_client_id=F("doctor__client_id"),
                doctor_first_name=F("doctor__first_name"),
                doctor_last_name=F("doctor__last_name"),
                doctor_profile_image=F("doctor__profile_image"),
                doctor_gender=F("doctor__gender"),
                doctor_email=F("doctor__email"),
                doctor_contact_number=F("doctor__contact_number"),
                doctor_date_of_birth=F("doctor__date_of_birth"),
                doctor_specialty=F("doctor__specialty"),
                doctor_qualifications=F("doctor__qualifications"),
                doctor_address=F("doctor__address"),
                doctor_department=F("doctor__department"),
                patient_client_id=F("patient__client_id"),
                patient_first_name=F("patient__first_name"),
                patient_last_name=F("patient__last_name"),
                patient_gender=F("patient__gender"),
                patient_email=F("patient__email"),
                patient_contact_number=F("patient__contact_number"),
                patient_address=F("patient__address"),
                patient_date_of_birth=F("patient__date_of_birth"),
                patient_medical_history=F("patient__medical_history"),
            )
            .values(
                "client_id",
                "hospital_name",
                "name",
                "owner_name",
                "city",
                "address",
                "email",
                "phone",
                "password",
                "user_type",
                "profile_image",
                "user_logo",
                "last_login",
                "created_at",
                "updated_at",
                "is_active",
                "doctor_client_id",
                "doctor_first_name",
                "doctor_last_name",
                "doctor_profile_image",
                "doctor_gender",
                "doctor_email",
                "doctor_contact_number",
                "doctor_date_of_birth",
                "doctor_specialty",
                "doctor_qualifications",
                "doctor_address",
                "doctor_department",
                "patient_client_id",
                "patient_first_name",
                "patient_last_name",
                "patient_gender",
                "patient_email",
                "patient_contact_number",
                "patient_address",
                "patient_date_of_birth",
                "patient_medical_history",
            )
            .first()
        )  # Assuming there's only one hospital

        return [queryset]  # Return as a list of dictionaries

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)




class DepartmentNurseDataJoinView(generics.ListAPIView):

    def get_queryset(self):
        queryset = Nurse.objects.select_related('department__client').annotate(
            department_id_alias=F('department__department_id'), 
            department_name=F('department__department_name'),
            department_created_at=F('department__created_at'),
            department_updated_at=F('department__updated_at'),
            hospital_name=F('department__client__hospital_name') 
        ).values(
            'client_id',
            'nurse_id',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'contact_number',
            'created_at',
            'updated_at',
            'department__department_id',  
            'department_name',
            'department_created_at',
            'department_updated_at',
            'hospital_name', 
           
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)



