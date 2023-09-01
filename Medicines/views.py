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
            client_id = serializer.validated_data["client"]
            
            # Check if the same medicine name is already registered for the same client_id
            if Medicine.objects.filter(medicine_name=medicine_name, client_id=client_id).exists():
                return Response({"error": "Medicine with the same name for this client already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({"message": "Medicine registered successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
 #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   

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
    
    
    
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class ClientMedicineListView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")

        if not client_id:
            return Response(
                {"error": "client_id is required in the request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        medicine = Medicine.objects.filter(client_id=client_id)

        if not medicine.exists():
            return Response(
                {"error": f"No medicine found for client with id {client_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MedicineListSerializer(medicine, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    




class ClientMedicineListByIdView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        medicine_id = data.get("medicine_id")

        if not (medicine_id and client_id):
            return Response(
                {
                    "error": "Both medicine_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            medicine = Medicine.objects.get(
                client_id=client_id, medicine_id=medicine_id
            )
        except Medicine.DoesNotExist:
            return Response(
                {"error": "No Medicines found for the given criteria"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MedicineListSerializer(medicine)
        return Response({"Data": serializer.data})





# @get Toatl Count Medicine -Api by cliendID
class ClientTotalMedicineCountView(APIView):
    def post(self, request):
        client_id = request.data.get("client_id")  # Get client_id from request data

        if client_id is not None:
            total_count = Medicine.objects.filter(client_id=client_id).count()
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




class ClientMedicineUpdateIDView(APIView):
    def get_Medicine(self, client_id, medicine_id):
        try:
            return Medicine.objects.get(client_id=client_id, medicine_id=medicine_id)
        except Medicine.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        medicine_id = data.get("medicine_id")

        if not (medicine_id and client_id):
            return Response(
                {
                    "error": "Both medicine_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = self.get_Medicine(client_id, medicine_id)
        if not payment:
            return Response(
                {"error": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = MedicineUpdateSerializer(payment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "medicine updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        medicine_id = data.get("medicine_id")

        if not (medicine_id and client_id):
            return Response(
                {
                    "error": "Both medicine_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        medicine = self.get_Medicine(client_id, medicine_id)
        if not medicine:
            return Response(
                {"error": "medicine not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = MedicineUpdateSerializer(medicine, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "medicine updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class ClientMedicineDeleteByIDView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        medicine_id = data.get("medicine_id")

        if not (medicine_id and client_id):
            return Response(
                {
                    "error": "Both medicine_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            medicine = Medicine.objects.get(client_id=client_id, medicine_id=medicine_id)
            medicine.delete()
            return Response(
                {"message": "Medicine deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Medicine.DoesNotExist:
            return Response(
                {"error": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND
            )
            
            
            
