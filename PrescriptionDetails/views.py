from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from PrescriptionDetails.models import PrescriptionDetail

from .serializers import (
    PrescriptionCreateSerializer,
    PrescriptionListSerializer,
    PrescriptionUpdateSerializer,
)


class PrescriptionDetailsCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PrescriptionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Prescription detail added successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrescriptionDetailsListView(APIView):
    def get(self, request, *args, **kwargs):
        prescriptions = PrescriptionDetail.objects.all()
        serializer = PrescriptionListSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PrescriptionDetailsListByIdView(APIView):
    def get(self, request, pk, format=None):
        try:
            prescription_details = PrescriptionDetail.objects.filter(
                prescription_detail_id=pk
            )
            serializer = PrescriptionListSerializer(prescription_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PrescriptionDetail.DoesNotExist:
            return Response(
                {"error": "Prescription details not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

class PrescriptionsDetailsUpdateView(APIView):
    def get_object(self, pk):
        try:
            return PrescriptionDetail.objects.get(pk=pk)
        except PrescriptionDetail.DoesNotExist:
            return None

    def put(self, request, pk, format=None):
        prescription_detail = self.get_object(pk)
        if prescription_detail is None:
            return Response(
                {"error": "Prescription detail not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PrescriptionUpdateSerializer(
            prescription_detail, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Prescription detail updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        prescription_detail = self.get_object(pk)
        if prescription_detail is None:
            return Response(
                {"error": "Prescription detail not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PrescriptionUpdateSerializer(
            prescription_detail, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Prescription detail updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





class PrescriptionDetailDeleteView(APIView):
    def get_object(self, pk):
        try:
            return PrescriptionDetail.objects.get(pk=pk)
        except PrescriptionDetail.DoesNotExist:
            return None

    def delete(self, request, pk, format=None):
        prescription_detail = self.get_object(pk)
        if prescription_detail is None:
            return Response(
                {"error": "Prescription detail not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        prescription_detail.delete()
        return Response(
            {"message": "Prescription detail deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )