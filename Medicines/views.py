from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Medicines.models import Medicine


from .serializers import (
    MedicineListSerializer,
    MedicineRegisterSerializer,
    MedicineUpdateSerializer,
)


class MedicineRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MedicineRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            medicine_name = serializer.validated_data["medicine_name"]
            
            if Medicine.objects.filter(medicine_name=medicine_name).exists():
                return Response({"error": "Medicine with the same name already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({"message": "Medicine registered successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicineListView(APIView):
    def get(self, request, *args, **kwargs):
        medicines = Medicine.objects.all()
        serializer = MedicineListSerializer(medicines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MedicineListByIdView(APIView):
    def get(self, request, *args, **kwargs):
        medicine_id = kwargs.get("medicine_id")  # Get the medicine ID from the URL
        try:
            medicine = Medicine.objects.get(medicine_id=medicine_id)
            serializer = MedicineListSerializer(medicine)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Medicine.DoesNotExist:
            return Response(
                {"error": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND
            )


class MedicineUpdateView(APIView):
    def get_medicine(self, medicine_id):
        try:
            return Medicine.objects.get(medicine_id=medicine_id)
        except Medicine.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        medicine_id = kwargs.get("medicine_id")  # Get the medicine ID from the URL
        medicine = self.get_medicine(medicine_id)
        if medicine is None:
            return Response(
                {"error": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = MedicineUpdateSerializer(medicine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        medicine_id = kwargs.get("medicine_id")  # Get the medicine ID from the URL
        medicine = self.get_medicine(medicine_id)
        if medicine is None:
            return Response(
                {"error": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = MedicineUpdateSerializer(medicine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicineDeleteView(APIView):
    def get_medicine(self, medicine_id):
        try:
            return Medicine.objects.get(medicine_id=medicine_id)
        except Medicine.DoesNotExist:
            return None

    def delete(self, request, *args, **kwargs):
        medicine_id = kwargs.get("medicine_id")  # Get the medicine ID from the URL
        medicine = self.get_medicine(medicine_id)
        if medicine is None:
            return Response(
                {"error": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND
            )

        medicine.delete()
        return Response(
            {"message": "Medicine deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )




class TotalMedicineCountView(APIView):
    def get(self, request, *args, **kwargs):
        total_medicines = Medicine.objects.count()
        return Response({"total_medicines": total_medicines}, status=status.HTTP_200_OK)