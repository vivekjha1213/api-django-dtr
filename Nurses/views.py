from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import NurseListSerializer, NurseRegisterSerializer, NurseUpdateSerializer
from .models import Nurse

class NurseRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = NurseRegisterSerializer(data=request.data)
        
        if Nurse.objects.filter(contact_number=request.data.get('contact_number')).exists():
            return Response({"error": "Nurse with the same contact number already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Nurse registered successfully"}, status=status.HTTP_201_CREATED)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class ClientNurseDetailsListView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")

        if not client_id:
            return Response(
                {"error": "client_id is required in the request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        nurses = Nurse.objects.filter(client_id=client_id)

        if not nurses.exists():
            return Response(
                {"error": f"No nurses found for client with id {client_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = NurseListSerializer(nurses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class ClientNurseDetailsListByIdView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        nurse_id = data.get("nurse_id")

        if not (nurse_id and client_id):
            return Response(
                {
                    "error": "Both nurse_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            client_nurse = Nurse.objects.get(
                client_id=client_id, nurse_id=nurse_id
            )
        except Nurse.DoesNotExist:
            return Response(
                {"error": "No nurse found for the given criteria"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = NurseListSerializer(client_nurse)
        return Response({"Data": serializer.data})



# @get Toatl Count Nurse-Api by cliendID
class TotalNurseCountView(APIView):
    def post(self, request):
        client_id = request.data.get("client_id")  # Get client_id from request data

        if client_id is not None:
            total_count = Nurse.objects.filter(client_id=client_id).count()
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


class ClientNurseUpdateIDView(APIView):
    def get_nurse(self, client_id, nurse_id):
        try:
            return Nurse.objects.get(client_id=client_id, nurse_id=nurse_id)
        except Nurse.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        nurse_id = data.get("nurse_id")

        if not (nurse_id and client_id):
            return Response(
                {
                    "error": "Both nurse_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        nurse = self.get_nurse(client_id, nurse_id)
        if not nurse:
            return Response(
                {"error": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = NurseUpdateSerializer(nurse, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Nurse updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        nurse_id = data.get("nurse_id")

        if not (nurse_id and client_id):
            return Response(
                {
                    "error": "Both nurse_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        nurse = self.get_nurse(client_id, nurse_id)
        if not nurse:
            return Response(
                {"error": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = NurseUpdateSerializer(nurse, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Nurse updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class ClientNurseDeleteByIDView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        nurse_id = data.get("nurse_id")

        if not (nurse_id and client_id):
            return Response(
                {
                    "error": "Both nurse_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            nurse = Nurse.objects.get(client_id=client_id, nurse_id=nurse_id)
            nurse.delete()
            return Response(
                {"message": "Nurse deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Nurse.DoesNotExist:
            return Response(
                {"error": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND
            )
            
            