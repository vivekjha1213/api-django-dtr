
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from patients.models import Patient
from patients.serializers import (
    PatientListSerializer,
    PatientRegistrationSerializer,
    PatientSearchSerializer,
    PatientUpdateSerializer,
)


logger = logging.getLogger("patients.patient")



# - Endpoint: POST `/api/patients/register`
# -Description: Creates a new patient with the provided details.
class PatientRegistrationView(APIView):
    def post(self, request, format=None):
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





########################################################################################################################################################################
###############################################################################################################################################################################

#@Get Data by Client Id.....
def get_patients_by_client_id(client_id):
    return Patient.objects.filter(client_id=client_id)

class ClientPatientsListView(APIView):
    def post(self, request, *args, **kwargs):
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
        
        
        
        
# @get Total Count Patient api by clidID 
class TotalClientPatientsCountView(APIView):
    def post(self, request):
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
            
            
            
  #@ Patient Delete By Client ID and Patient ID...          
class ClientPatientDeleteViewId(APIView):
    def post(self, request):
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
          
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
          
  #@ Patient Update  By Client ID and Patient ID.....         
class ClientPatientUpdateView(APIView):
    def update_patient(self, patient, data):
        serializer = PatientUpdateSerializer(patient, data=data, partial=True)
        if serializer.is_valid():
            updated_patient = serializer.save()
            return Response(
                {"message": "Patient profile updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
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
         
         
    
 # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++      
            
#@get seprate patient By- clientId & Patient_id...      
class ClientPatientsListByIDView(APIView):
    def post(self, request, *args, **kwargs):
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
    
   
  # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
   
   
   
 # Search Api...................... by client id and    patient id and patient firstname, last_name..
 
class ClientPatientSearchView(APIView):
    def get(self, request):
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
    
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++