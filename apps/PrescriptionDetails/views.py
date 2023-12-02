import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics
from apps.PrescriptionDetails.models import PrescriptionDetail

from .serializers import (
    PrescriptionCreateSerializer,
    PrescriptionListSerializer,
    PrescriptionUpdateSerializer,
)


# logger = logging.getLogger("PrescriptionDetails.PrescriptionDetail")


class PrescriptionDetailsCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PrescriptionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Prescription detail added successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientPrescriptionDetailsListView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")

        if not client_id:
            return Response(
                {"error": "client_id is required in the request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        prepsciptions = PrescriptionDetail.objects.filter(client_id=client_id)

        if not prepsciptions.exists():
            return Response(
                {"error": f"No prepsciptions found for client with id {client_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PrescriptionListSerializer(prepsciptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientPrescriptionDetailsListByIdView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        prescription_detail_id = data.get("prescription_detail_id")

        if not (prescription_detail_id and client_id):
            return Response(
                {
                    "error": "Both prescription_detail_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            prescriptionDetail = PrescriptionDetail.objects.get(
                client_id=client_id, prescription_detail_id=prescription_detail_id
            )
        except PrescriptionDetail.DoesNotExist:
            return Response(
                {"error": "No prescriptionDetails found for the given criteria"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PrescriptionListSerializer(prescriptionDetail)
        return Response({"Data": serializer.data})

class TotalPrescriptionDetailCountView(APIView):
    def post(self, request):
        client_id = request.data.get("client_id")  # Get client_id from request data

        if client_id is not None:
            total_count = PrescriptionDetail.objects.filter(client_id=client_id).count()
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

class ClientPrescriptionDetailUpdateIDView(APIView):
    def get_PrescriptionDetail(self, client_id, prescription_detail_id):
        try:
            return PrescriptionDetail.objects.get(
                client_id=client_id, prescription_detail_id=prescription_detail_id
            )
        except PrescriptionDetail.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        prescription_detail_id = data.get("prescription_detail_id")

        if not (prescription_detail_id and client_id):
            return Response(
                {
                    "error": "Both prescription_detail_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = self.get_PrescriptionDetail(client_id, prescription_detail_id)
        if not payment:
            return Response(
                {"error": "PrescriptionDetail not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PrescriptionUpdateSerializer(payment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "PrescriptionDetail updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        prescription_detail_id = data.get("prescription_detail_id")

        if not (prescription_detail_id and client_id):
            return Response(
                {
                    "error": "Both prescription_detail_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        prescriptionDetail = self.get_PrescriptionDetail(
            client_id, prescription_detail_id
        )
        if not prescriptionDetail:
            return Response(
                {"error": "PrescriptionDetail not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PrescriptionUpdateSerializer(
            prescriptionDetail, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "PrescriptionDetail updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientPrescriptionDetailDeleteByIDView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        prescription_detail_id = data.get("prescription_detail_id")

        if not (prescription_detail_id and client_id):
            return Response(
                {
                    "error": "Both prescription_detail_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            prescriptionDetail = PrescriptionDetail.objects.get(
                client_id=client_id, prescription_detail_id=prescription_detail_id
            )
            prescriptionDetail.delete()
            return Response(
                {"message": "PrescriptionDetail deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except PrescriptionDetail.DoesNotExist:
            return Response(
                {"error": "PrescriptionDetail not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
            
class PrescriptionDetailPrescriptionsJoin(generics.ListAPIView):
    serializer_class = None
    
    def get_queryset(self):
        client_id = self.kwargs.get('client_id')        
        queryset = PrescriptionDetail.objects.select_related(
            "prescription",
            "medicine"
        ).values(
             "prescription_detail_id",
            "prescription__prescription_id",
            "prescription__prescription_date",
            "prescription__prescription_time",
            "prescription__notes",
            "prescription__created_at",
            "prescription__updated_at",
            "prescription__patient__patient_id",
            "prescription__patient__first_name",
            "prescription__patient__last_name",
            "prescription__patient__gender",
            "prescription__patient__email",
            "prescription__patient__contact_number",
            "prescription__patient__date_of_birth",
            "prescription__doctor__doctor_id",
            "prescription__doctor__first_name",
            "prescription__doctor__last_name",
            "prescription__doctor__profile_image", 
            "prescription__doctor__gender",
            "prescription__doctor__email",
            "prescription__doctor__contact_number",
            "prescription__doctor__date_of_birth",
            "prescription__client__client_id",
            "medicine_id",
            "medicine__medicine_name", 
            "medicine__unit_price",
            "medicine__stock_quantity",  
            "dosage",
            "frequency",
            "client_id",
        ).filter(client_id=client_id) 

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "client_id not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(queryset)