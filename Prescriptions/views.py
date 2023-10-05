import logging
from Prescriptions.models import Prescription
from Prescriptions.serializers import (
    PrescriptionCreateSerializer,
    PrescriptionListSerializer,
    PrescriptionUpdateSerializer,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics


logger = logging.getLogger("Prescriptions.Prescription")




class PrescriptionCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PrescriptionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Prescription added successfully."
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class ClientPrescriptionsListView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")

        if not client_id:
            return Response(
                {"error": "client_id is required in the request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        prescriptions = Prescription.objects.filter(client_id=client_id)
        
        if not prescriptions.exists():  # Corrected this line
            return Response(
                {"error": f"No prescriptions found for client with id {client_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PrescriptionListSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class ClientPrescriptionsListByIdView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        prescription_id = data.get("prescription_id")

        if not (prescription_id and client_id):
            return Response(
                {
                    "error": "Both prescription_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            prescriptions = Prescription.objects.get(
                client_id=client_id, prescription_id=prescription_id
            )
        except Prescription.DoesNotExist:
            return Response(
                {"error": "No prescriptionss found for the given criteria"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PrescriptionListSerializer(prescriptions)
        return Response({"Data": serializer.data})


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# @get Toatl Count PrescriptionDetail -Api by cliendID
class TotalPrescriptionSCountView(APIView):
    def post(self, request):
        client_id = request.data.get("client_id")  # Get client_id from request data

        if client_id is not None:
            total_count = Prescription.objects.filter(client_id=client_id).count()
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



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




class ClientPrescriptionUpdateIDView(APIView):
    def get_Prescription(self, client_id, prescription_id):
        try:
            return Prescription.objects.get(client_id=client_id, prescription_id=prescription_id)
        except Prescription.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        prescription_id = data.get("prescription_id")

        if not (prescription_id and client_id):
            return Response(
                {
                    "error": "Both prescription_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        prescription = self.get_Prescription(client_id, prescription_id)
        if not prescription:
            return Response(
                {"error": "prescription not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PrescriptionUpdateSerializer(prescription, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Prescription updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        prescription_id = data.get("prescription_id")

        if not (prescription_id and client_id):
            return Response(
                {
                    "error": "Both prescription_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        prescriptionDetail = self.get_Prescription(client_id, prescription_id)
        if not prescriptionDetail:
            return Response(
                {"error": "Prescription not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PrescriptionUpdateSerializer(prescriptionDetail, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Prescription updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



class ClientPrescriptionDeleteByIDView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        prescription_id = data.get("prescription_id")

        if not (prescription_id and client_id):
            return Response(
                {
                    "error": "Both prescription_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            prescription = Prescription.objects.get(client_id=client_id, prescription_id=prescription_id)
            prescription.delete()
            return Response(
                {"message": "prescription deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Prescription.DoesNotExist:
            return Response(
                {"error": "prescription not found"}, status=status.HTTP_404_NOT_FOUND
            )
            
            
#-----------------------------------------------------------------------------------------------------------------


class JoinListPrescriptionsListView(generics.ListAPIView):
    def get_queryset(self):
        client_id = self.request.data.get("client_id")
        
        if client_id is not None:
            queryset = Prescription.objects.filter(client_id=client_id).select_related("patient", "doctor")
            return queryset

        return Prescription.objects.none()  # Return an empty queryset if client_id is not provided.

    def post(self, request, *args, **kwargs):
        client_id = self.request.data.get("client_id")
        queryset = self.get_queryset()
        data = list(queryset.values(
            "prescription_id",
            "prescription_date",
            "notes",
            "patient_id",
            "patient__first_name",
            "patient__last_name",
            "doctor_id",
            "doctor__first_name",
            "doctor__last_name",
            "created_at",
            "updated_at",
            "client_id",
        ))

        if not data:
            return Response(
                {"detail": f"No Prescriptions found for client_id: {client_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(data)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++