import logging
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator



from rest_framework.views import APIView
from Hospitals.permissions import UnrestrictedPermission
from doctors.models import Doctor
from doctors.serializers import (
    DoctorListSerializer,
    DoctorRegistrationSerializer,
    DoctorSearchSerializer,
    DoctorUpdateSerializer,
)

logger = logging.getLogger("doctors.doctor")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Rest-Api---DRF.......
# Dr-Register Api......
class DoctorRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = DoctorRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            if Doctor.objects.filter(email=email).exists():
                return Response(
                    {
                        "success": False,
                        "message": "A doctor with this email already exists.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()

            return Response(
                {"success": True, "message": "Registration Success"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"success": False, "message": "Registration Failure"},
            status=status.HTTP_400_BAD_REQUEST,
        )


##################################################################################################################################################################################################

#################################################################################################################################################


# @Get Data by Client Id.....
def get_doctors_by_client_id(client_id):
    return Doctor.objects.filter(client_id=client_id)


class ClientDoctorListView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")

        if client_id:
            doctors = get_doctors_by_client_id(client_id)

            if doctors.exists():
                serializer = DoctorListSerializer(doctors, many=True)
                return Response({"Data": serializer.data})
            else:
                return Response(
                    {"error": "No doctors found for the given client_id"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": "client_id is missing in the request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# @get Toatl Count doctor api by clidID
class TotalClientDoctorCountView(APIView):
    def post(self, request):
        client_id = request.data.get("client_id")  # Get client_id from request data

        if client_id is not None:
            total_count = Doctor.objects.filter(client_id=client_id).count()
            return Response(
                {"success": True, "total_count": total_count}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "client_id is required in the request data",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# @ Patient Delete By Client ID and Patient ID...
class ClientDoctorDeleteViewId(APIView):
    def post(self, request):
        doctor_id = request.data.get("doctor_id")  # Get doctor_id from request data
        client_id = request.data.get("client_id")  # Get client_id from request data

        if doctor_id is not None and client_id is not None:
            try:
                patient = Doctor.objects.get(doctor_id=doctor_id, client_id=client_id)
                patient.delete()
                return Response(
                    {"success": True, "message": "Profile deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except Doctor.DoesNotExist:
                return Response(
                    {"success": False, "message": "Profile does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Both doctor_id and client_id are required in the request data",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Update all dr by doctor_id  and client Id......:
class ClientDoctorUpdateView(APIView):
    def update_doctor(self, doctor, data):
        serializer = DoctorUpdateSerializer(doctor, data=data, partial=True)
        if serializer.is_valid():
            updated_doctor = serializer.save()
            return Response(
                {"message": "Doctor profile updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        doctor_id = request.data.get("doctor_id")
        client_id = request.data.get("client_id")

        if doctor_id and client_id:
            try:
                doctor = Doctor.objects.get(doctor_id=doctor_id, client_id=client_id)
            except Doctor.DoesNotExist:
                return Response(
                    {"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND
                )
            return self.update_doctor(doctor, request.data)
        else:
            return Response(
                {
                    "error": "Both doctor_id and client_id are required in the request data."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, *args, **kwargs):
        doctor_id = request.data.get("doctor_id")
        client_id = request.data.get("client_id")

        if doctor_id and client_id:
            try:
                doctor = Doctor.objects.get(doctor_id=doctor_id, client_id=client_id)
            except Doctor.DoesNotExist:
                return Response(
                    {"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND
                )
            return self.update_doctor(doctor, request.data)
        else:
            return Response(
                {
                    "error": "Both doctor_id and client_id are required in the request data."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class ClientDoctorListByIDView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        doctor_id = data.get("doctor_id")

        if not (doctor_id and client_id):
            return Response(
                {
                    "error": "Both doctor_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        doctors = Doctor.objects.filter(client_id=client_id)

        if doctor_id:
            doctors = doctors.filter(doctor_id=doctor_id)

        serializer = DoctorListSerializer(doctors, many=True)
        return Response({"Data": serializer.data})


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Search Api...................... by client id and    patient id and patient firstname, last_name..
class ClientDoctorSearchView(APIView):
    def get(self, request):
        search_query = request.GET.get("query")
        client_id = request.GET.get("client_id")  # New client_id parameter

        if not search_query:
            return Response(
                {"success": False, "message": "Search query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        doctors = Doctor.objects.filter(
            first_name__icontains=search_query, client=client_id
        )

        serializer = DoctorSearchSerializer(doctors, many=True)
        response_data = {
            "success": True,
            "count": len(doctors),
            "results": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# class DoctorListView(APIView):
#     permission_classes = [UnrestrictedPermission]
#     def get(self, request, format=None):
#         doctors = Doctor.objects.all()
#         serializer = DoctorListSerializer(doctors, many=True)
#         # Return the serialized data as a JSON response
#         return Response({"Data": serializer.data})


# cache redis implement here
@method_decorator(cache_page(60), name="get")
class DoctorListView(APIView):
    permission_classes = [UnrestrictedPermission]

    def get(self, request, format=None):
        doctors = Doctor.objects.all()
        serializer = DoctorListSerializer(doctors, many=True)
        # Return the serialized data as a JSON response
        return Response({"Data": serializer.data})


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def get_doctors_by_client_id(client_id):
    return Doctor.objects.filter(client_id=client_id)


class AllClientDoctorListView(APIView):
    permission_classes = [UnrestrictedPermission]

    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")

        if client_id:
            doctors = get_doctors_by_client_id(client_id)

            if doctors.exists():
                serializer = DoctorListSerializer(doctors, many=True)
                return Response({"Data": serializer.data})
            else:
                return Response(
                    {"error": "No doctors found for the given client_id"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": "client_id is missing in the request data"},
                status=status.HTTP_400_BAD_REQUEST,
     
            )
            
            
            