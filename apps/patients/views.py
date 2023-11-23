
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.Hospitals.permissions import UnrestrictedPermission
from apps.patients.models import Patient
from apps.patients.serializers import (
    PatientCompaignSerializer,
    PatientListSerializer,
    PatientRegistrationSerializer,
    PatientSearchSerializer,
    PatientUpdateSerializer,
)


# logger = logging.getLogger("patients.patient")

class PatientRegistrationView(APIView):
    """
    Registers a new patient.

    Request:
    - 'POST' method is used to register a patient.
    - Requires patient data in the request body.

    Response:
    - Upon successful registration, returns a success message.
    - If the provided email already exists, returns an error message.
    - In case of invalid data, returns the serialization errors.

    Example:
    - An example of a successful patient registration request.
    """
    def post(self, request, format=None):
        """
        Registers a new patient.

        :param request: HTTP request object.
        :param format: Format suffix, not used here.

        :return: JSON response indicating the registration status.
        """
        serializer = PatientRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            if Patient.objects.filter(email=email).exists():
                return Response(
                    {"success": False, "message": "This email already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()

            return Response(
                {"success": True, "message": "Registration successful"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"success": False, "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


def get_patients_by_client_id(client_id):
    """
    Retrieves patients by client ID.

    :param client_id: ID of the client.

    :return: QuerySet of patients belonging to the given client ID.
    """
    return Patient.objects.filter(client_id=client_id)

class ClientPatientsListView(APIView):
    """
    Retrieves a list of patients belonging to a specific client.

    Request:
    - 'POST' method is used to retrieve patients by client ID.
    - Requires 'client_id' in the request body.

    Response:
    - Returns patient data associated with the client if found.
    - If no patients are found for the provided client ID, returns a 'Not Found' response.
    - If 'client_id' is missing in the request data, returns a 'Bad Request' response.

    Example:
    - An example of retrieving patients by client ID.
    """
    def post(self, request, *args, **kwargs):
        """
        Retrieves a list of patients belonging to a specific client.

        :param request: HTTP request object.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.

        :return: JSON response containing patient data or error messages.
        """
        data = request.data
        client_id = data.get("client_id")
        
        if client_id:
            patients = get_patients_by_client_id(client_id)
            
            if patients.exists():
                serializer = PatientListSerializer(patients, many=True)
                return Response({"Data": serializer.data})
            else:
                return Response({"error": "No patients found for the given client_id"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "client_id is missing in the request data"}, status=status.HTTP_400_BAD_REQUEST)
        

class TotalClientPatientsCountView(APIView):
    """
    Retrieves the total count of patients for a specific client.

    Request:
    - 'POST' method is used to retrieve the total count of patients by client ID.
    - Requires 'client_id' in the request body.

    Response:
    - Returns the total count of patients associated with the client if found.
    - If 'client_id' is missing in the request data, returns a 'Bad Request' response.

    Example:
    - An example of retrieving the total count of patients by client ID.
    """
    def post(self, request):
        """
        Retrieves the total count of patients for a specific client.

        :param request: HTTP request object.

        :return: JSON response containing the total count of patients or an error message.
        """
        client_id = request.data.get("client_id")  # Get client_id from request data
        
        if client_id is not None:
            total_count = Patient.objects.filter(client_id=client_id).count()
            return Response(
                {"success": True, "total_count": total_count},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"success": False, "message": "client_id is required in the request data"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
                      
          
class ClientPatientDeleteViewId(APIView):
    """
    Deletes a patient profile associated with a client by their IDs.

    Request:
    - 'POST' method is used for deleting a patient profile.
    - Requires 'patient_id' and 'client_id' in the request body.

    Response:
    - Deletes the patient profile if it exists.
    - If the patient profile does not exist for the provided IDs, returns a 'Not Found' response.
    - If 'patient_id' and 'client_id' are missing in the request data, returns a 'Bad Request' response.

    Example:
    - An example of deleting a patient profile by its ID and client ID.
    """
    def post(self, request):
        """
        Deletes a patient profile associated with a client by their IDs.

        :param request: HTTP request object.

        :return: JSON response indicating success or error messages.
        """
        patient_id = request.data.get("patient_id")  # Get patient_id from request data
        client_id = request.data.get("client_id")  # Get client_id from request data
        
        if patient_id is not None and client_id is not None:
            try:
                patient = Patient.objects.get(patient_id=patient_id, client_id=client_id)
                patient.delete()
                return Response(
                    {"success": True, "message": "Profile deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except Patient.DoesNotExist:
                return Response(
                    {"success": False, "message": "Profile does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"success": False, "message": "Both patient_id and client_id are required in the request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )
          
        
class ClientPatientUpdateView(APIView):
    """
    Updates a patient profile associated with a client by their IDs.

    Request:
    - 'PUT' and 'PATCH' methods are used for updating a patient profile.
    - Requires 'patient_id' and 'client_id' in the request body.

    Response:
    - Updates the patient profile if it exists.
    - If the patient profile does not exist for the provided IDs, returns a 'Not Found' response.
    - If 'patient_id' and 'client_id' are missing in the request data, returns a 'Bad Request' response.

    Example:
    - An example of updating a patient profile by its ID and client ID using 'PUT' or 'PATCH'.
    """
    def update_patient(self, patient, data):
        """
        Updates the patient profile.

        :param patient: Patient object to be updated.
        :param data: Data to update the patient object.

        :return: JSON response indicating success or error messages.
        """
        serializer = PatientUpdateSerializer(patient, data=data, partial=True)
        if serializer.is_valid():
            updated_patient = serializer.save()
            return Response(
                {"message": "Patient profile updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        Handles 'PUT' request to update a patient profile.

        :param request: HTTP request object.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.

        :return: JSON response indicating success or error messages.
        """
        patient_id = request.data.get("patient_id")
        client_id = request.data.get("client_id")
        
        if patient_id and client_id:
            try:
                patient = Patient.objects.get(patient_id=patient_id, client_id=client_id)
            except Patient.DoesNotExist:
                return Response(
                    {"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND
                )
            return self.update_patient(patient, request.data)
        else:
            return Response(
                {"error": "Both patient_id and client_id are required in the request data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, *args, **kwargs):
        """
        Handles 'PATCH' request to update a patient profile.

        :param request: HTTP request object.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.

        :return: JSON response indicating success or error messages.
        """
        patient_id = request.data.get("patient_id")
        client_id = request.data.get("client_id")
        
        if patient_id and client_id:
            try:
                patient = Patient.objects.get(patient_id=patient_id, client_id=client_id)
            except Patient.DoesNotExist:
                return Response(
                    {"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND
                )
            return self.update_patient(patient, request.data)
        else:
            return Response(
                {"error": "Both patient_id and client_id are required in the request data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

     
class ClientPatientsListByIDView(APIView):
    """
    Retrieves patient data based on client_id and patient_id.

    Request:
    - 'POST' method is used for fetching patient data.
    - Requires 'patient_id' and 'client_id' in the request body.

    Response:
    - Returns patient data for the given client_id and patient_id.
    - If 'patient_id' and 'client_id' are missing in the request data, returns a 'Bad Request' response.

    Example:
    - An example of retrieving patient data by client_id and patient_id.
    """
    def post(self, request, *args, **kwargs):
        """
        Retrieves patient data based on client_id and patient_id.

        :param request: HTTP request object.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.

        :return: JSON response containing patient data for the given client_id and patient_id.
        """
        data = request.data
        client_id = data.get("client_id")
        patient_id = data.get("patient_id")
        
        if not (patient_id and client_id):
            return Response({"error": "Both patient_id and client_id are required in the request data"}, status=status.HTTP_400_BAD_REQUEST)
        
        patients = Patient.objects.filter(client_id=client_id)
        
        if patient_id:
            patients = patients.filter(patient_id=patient_id)
            
        serializer = PatientListSerializer(patients, many=True)
        return Response({"Data": serializer.data})
    
   
class ClientPatientSearchView(APIView):
    """
    Searches for patients based on a query string and client_id.

    Request:
    - 'GET' method is used for searching patients.
    - Requires 'query' and 'client_id' as query parameters in the URL.

    Response:
    - Returns search results based on the query string and client_id.
    - If the query parameter is missing, returns a 'Bad Request' response.

    Example:
    - An example of searching for patients using a query string and client_id.
    """

    def get(self, request):
        """
        Searches for patients based on a query string and client_id.

        :param request: HTTP request object.

        :return: JSON response containing search results based on the query string and client_id.
        """
        search_query = request.GET.get("query")
        client_id = request.GET.get("client_id")  # New client_id parameter
        
        if not search_query:
            return Response(
                {"success": False, "message": "Search query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        patients = Patient.objects.filter(first_name__icontains=search_query, client=client_id)
        
        serializer = PatientSearchSerializer(patients, many=True)
        response_data = {
            "success": True,
            "count": len(patients),
            "results": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
 
 
class PatientCompaignAPIView(APIView):
    """
    Registers a patient and performs a campaign.

    Permission:
    - UnrestrictedPermission is required to access this endpoint.

    Request:
    - 'POST' method is used for patient registration and campaign.

    Response:
    - Registers a new patient and performs a campaign if the email does not already exist.
    - If the email already exists, returns a success message.
    - If validation fails for the serializer, returns errors.

    Example:
    - An example of registering a patient and performing a campaign.
    """
    permission_classes = [UnrestrictedPermission]

    def post(self, request, format=None):
        """
        Registers a patient and performs a campaign.

        :param request: HTTP request object.
        :param format: Format of the request.

        :return: JSON response indicating success or error messages.
        """
        email = request.data.get('email')
        
        # Check if a patient with the same email already exists
        existing_patient = Patient.objects.filter(email=email).first()

        if existing_patient:
            return Response({"message": "Registration successful (email already exists)"}, status=status.HTTP_201_CREATED)

        serializer = PatientCompaignSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
