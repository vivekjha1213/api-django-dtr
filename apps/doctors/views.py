import logging
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator



from rest_framework.views import APIView
from apps.Hospitals.permissions import UnrestrictedPermission
from apps.Middleware.CustomPagination import PagePagination
from apps.doctors.models import Doctor
from apps.doctors.serializers import (
    DoctorListSerializer,
    DoctorRegistrationSerializer,
    DoctorSearchSerializer,
    DoctorUpdateSerializer,
)

# logger = logging.getLogger("doctors.doctor")




class DoctorRegistrationView(APIView):
    """
    View to handle the registration of a new doctor.

    On receiving a POST request with doctor registration data, this view
    validates the provided data using DoctorRegistrationSerializer. It checks
    if a doctor with the same email already exists. If not, it saves the new
    doctor's details in the database.

    Request data:
    - email: The email address of the new doctor.

    Returns:
    - Upon successful registration, returns a success message with status 201.
    - If the provided email already exists, returns an error message with status 400.
    - In case of invalid data, returns a failure response with status 400.

   
    """
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


def get_doctors_by_client_id(client_id):
    """
    Retrieve doctors associated with a specific client using client_id.

    Parameters:
    - client_id: ID of the client

    Returns:
    - QuerySet: QuerySet containing doctors associated with the specified client_id
    """
    return Doctor.objects.filter(client_id=client_id)


class ClientDoctorListView(APIView):
    """
    API endpoint to retrieve a list of doctors associated with a specific client.

    Parameters:
    - request: Request object containing the client_id in the data.

    Returns:
    - Response: JSON response containing a list of doctors for the given client.
    """
    pagination_class =PagePagination
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


class TotalClientDoctorCountView(APIView):
    """
        Get the total count of doctors associated with a specific client.
        Parameters:
        - request: Request object containing the client_id in the data.

        Returns:
        - Response: JSON response containing the total count of doctors for the given client.
    """
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

class ClientDoctorDeleteViewId(APIView):
    def post(self, request):
        """
        Delete a doctor's profile.

        This method deletes the doctor's profile with the specified doctor_id and client_id.

        Args:
            request: The HTTP request object.

        Returns:
            A JSON response with a success message or an error message.
        """
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


class ClientDoctorUpdateView(APIView):
    """
    An abstract class for creating REST API views.

    This class provides a number of methods and attributes that are useful for creating API views,
    including:

        * `get`: Handles GET requests.
        * `post`: Handles POST requests.
        * `put`: Handles PUT requests.
        * `patch`: Handles PATCH requests.
        * `delete`: Handles DELETE requests.

    APIView classes can also be subclassed to create custom API views.

    Attributes:
        lookup_field: The field to use for looking up objects in the database.
        serializer_class: The serializer class to use for serializing and deserializing data.
        filter_backends: A list of filter backend classes to use for filtering querysets.
        authentication_classes: A list of authentication backend classes to use for authentication.
        permission_classes: A list of permission backend classes to use for checking permissions.

    Methods:
        initialize(request, *args, **kwargs): Initializes the view instance.
        get(request, *args, **kwargs): Handles GET requests.
        post(request, *args, **kwargs): Handles POST requests.
        put(request, *args, **kwargs): Handles PUT requests.
        patch(request, *args, **kwargs): Handles PATCH requests.
        delete(request, *args, **kwargs): Handles DELETE requests.
        options(request, *args, **kwargs): Handles OPTIONS requests.
        finalize(request, *args, **kwargs): Finalizes the view instance.
    """
    def update_doctor(self, doctor, data):
        """
        Update a doctor's information.

        This method updates the doctor's information with the data provided in the `data` dictionary.

        Args:
            doctor: The doctor object to be updated.
            data: A dictionary containing the updated doctor information.

        Returns:
            A JSON response with the updated doctor information or an error message.
        """
        serializer = DoctorUpdateSerializer(doctor, data=data, partial=True)
        if serializer.is_valid():
            updated_doctor = serializer.save()
            return Response(
                {"message": "Doctor profile updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        put a doctor's information.

        This method updates the doctor's information with the data provided in the request body.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            A JSON response with the updated doctor information or an error message.
        """
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
        """
        Patch a doctor's information.

        This method updates the doctor's information with the data provided in the request body.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            A JSON response with the updated doctor information or an error message.
        """
    
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

class ClientDoctorListByIDView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Retrieve a list of doctors by a specific client ID and/or doctor ID.

        Parameters:
        - request: Request object.
        - client_id (str): Unique identifier for the client.
        - doctor_id (str): Unique identifier for the doctor.

        Returns:
        - Response: JSON response containing a list of doctors filtered by the specified client ID and/or doctor ID.
        """
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


class ClientDoctorSearchView(APIView):
     
    def get(self, request):
        """
        Retrieve a list of doctors based on a search query and a client ID.

        Parameters:
        - request: Request object.
        - query (str): Search query parameter.
        - client_id (str): Unique identifier for the client.

        Returns:
        - Response: JSON response containing the list of doctors that match the search query for the specified client.
        """
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


# class DoctorListView(APIView):
#     permission_classes = [UnrestrictedPermission]
#     def get(self, request, format=None):
#         doctors = Doctor.objects.all()
#         serializer = DoctorListSerializer(doctors, many=True)
#         # Return the serialized data as a JSON response
#         return Response({"Data": serializer.data})




# cache redis implement here
''' 
class DoctorListView(APIView):
    permission_classes = [UnrestrictedPermission]


    def get(self, request, format=None):
        
        redis_cache_middleware = RedisQueryCacheMiddleware(self.get_response, cache_duration=600)  # 600 seconds = 10 minutes
        response = redis_cache_middleware(request)
        
        doctors = Doctor.objects.all()
        serializer = DoctorListSerializer(doctors, many=True)
        # Return the serialized data as a JSON response
        return Response({"Data": serializer.data})

'''


#@cache example......

class DoctorListView(APIView):
    
    permission_classes = [UnrestrictedPermission]

    @method_decorator(cache_page(600))  
    
    def get(self, request, format=None):
        """
        Retrieve a list of all doctors and serialize the data.

        Parameters:
        - request: Request object.
        - format (str, optional): The format of the request. Defaults to None.

        Returns:
        - Response: JSON response containing serialized Doctor data.
        """
        doctors = Doctor.objects.all()
        serializer = DoctorListSerializer(doctors, many=True)
        # Return the serialized data as a JSON response
        return Response({"Data": serializer.data})

def get_doctors_by_client_id(client_id):
    """
    Retrieves all doctors associated with a specific client.

    Parameters:
    - client_id (int): The unique identifier of the client.

    Returns:
    - QuerySet: QuerySet containing Doctor objects filtered by the client ID.
    """
    return Doctor.objects.filter(client_id=client_id)

class AllClientDoctorListView(APIView):
    """
    API endpoint to retrieve all doctors associated with a specific client.
    """
    permission_classes = [UnrestrictedPermission]

    def post(self, request, *args, **kwargs):
        """
        Retrieve all doctors based on a client ID.

        Parameters:
        - request (Request): Django request object containing client ID data.
        - args: Variable-length argument list.
        - kwargs: Arbitrarily named arguments.

        Returns:
        - Response: JSON response containing the list of doctors filtered by client ID.
        """
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
            


class ClientDoctorCompaign(APIView):
    """
    API endpoint to retrieve doctors associated with a specific client or client and doctor ID combination.
    """
    permission_classes = [UnrestrictedPermission]
    def post(self, request, *args, **kwargs):
        """
        Retrieve doctors based on client and/or doctor ID.

        Parameters:
        - request (Request): Django request object containing client and doctor ID data.
        - args: Variable-length argument list.
        - kwargs: Arbitrarily named arguments.

        Returns:
        - Response: JSON response containing the list of doctors filtered by client and/or doctor ID.
        """
        data = request.data
        client_id = data.get("client_id")
        doctor_id = data.get("doctor_id")
        
        if not (doctor_id and client_id):
            return Response({"error": "Both doctor_id and client_id are required in the request data"}, status=status.HTTP_400_BAD_REQUEST)
        
        doctors = Doctor.objects.filter(client_id=client_id)
        
        if doctor_id:
            doctors = doctors.filter(doctor_id=doctor_id)
            
        serializer = DoctorListSerializer(doctors, many=True)
        return Response({"Data": serializer.data})
    
            