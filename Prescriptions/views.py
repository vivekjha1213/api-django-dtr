from Prescriptions.models import Prescription
from Prescriptions.serializers import (
    PrescriptionCreateSerializer,
    PrescriptionListSerializer,
    PrescriptionUpdateSerializer,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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







class PrescriptionListView(APIView):
    def get(self, request, *args, **kwargs):
        prescriptions = Prescription.objects.all()
        serializer = PrescriptionListSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PrescriptionListIdView(APIView):
    def get(self, request, *args, **kwargs):
        prescription_id = kwargs.get("prescription_id")

        if prescription_id is not None:
            try:
                prescription = Prescription.objects.get(pk=prescription_id)
                serializer = PrescriptionListSerializer(prescription)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Prescription.DoesNotExist:
                return Response(
                    {"error": "Prescription not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        prescriptions = Prescription.objects.all()
        serializer = PrescriptionListSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class PrescriptionUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Prescription.objects.get(pk=pk)
        except Prescription.DoesNotExist:
            return None

    def put(self, request, pk, format=None):
        prescription = self.get_object(pk)
        if prescription is None:
            return Response({"error": "Prescription not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PrescriptionUpdateSerializer(prescription, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Prescription updated successfully."
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        prescription = self.get_object(pk)
        if prescription is None:
            return Response({"error": "Prescription not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PrescriptionUpdateSerializer(prescription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Prescription updated successfully."
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class PrescriptiondeleteView(APIView):
    def get_object(self, pk):
        try:
            return Prescription.objects.get(pk=pk)
        except Prescription.DoesNotExist:
            return None

    def delete(self, request, pk, format=None):
        prescription = self.get_object(pk)
        if prescription is None:
            return Response({"error": "Prescription not found"}, status=status.HTTP_404_NOT_FOUND)

        prescription.delete()
        return Response({"message": "Prescription deleted successfully."}, status=status.HTTP_204_NO_CONTENT)