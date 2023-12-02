import logging
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import LabTest
from .serializers import (
    LabTestCreateSerializer,
    LabTestListSerializer,
    LabTestUpdateSerializer,
)



logger = logging.getLogger("LabTests.LabTest")



class LabTestCreateView(APIView):
    def post(self, request, format=None):
        serializer = LabTestCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Lab test created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ClientLabTestDetailsListView(APIView):
    def post(self, request, *args, **kwargs):
        client_id = request.data.get(
            "client_id"
        )  # Get the client_id from the request data

        if not client_id:
            return Response(
                {"error": "client_id is required in the request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        labTest = LabTest.objects.filter(client_id=client_id)

        if not labTest.exists():
            return Response(
                {"error": f"No LabTest found for client with id {client_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LabTestListSerializer(labTest, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClientTestDetailsListByIdView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        lab_test_id = data.get("lab_test_id")

        if not (lab_test_id and client_id):
            return Response(
                {
                    "error": "Both lab_test_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            client_lab_test = LabTest.objects.get(
                client_id=client_id, lab_test_id=lab_test_id
            )
        except LabTest.DoesNotExist:
            return Response(
                {"error": "No lab test found for the given criteria"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LabTestListSerializer(client_lab_test)
        return Response({"Data": serializer.data})


class TotalLabTestCountView(APIView):
    def post(self, request):
        client_id = request.data.get("client_id")  # Get client_id from request data

        if client_id is not None:
            total_count = LabTest.objects.filter(client_id=client_id).count()
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


class ClientLabTestUpdateIDView(APIView):
    def get_lab_test(self, client_id, lab_test_id):
        try:
            return LabTest.objects.get(client_id=client_id, lab_test_id=lab_test_id)
        except LabTest.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        lab_test_id = data.get("lab_test_id")

        if not (lab_test_id and client_id):
            return Response(
                {
                    "error": "Both lab_test_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        lab_test = self.get_lab_test(client_id, lab_test_id)
        if not lab_test:
            return Response(
                {"error": "Lab test not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = LabTestUpdateSerializer(lab_test, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Lab test updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        lab_test_id = data.get("lab_test_id")

        if not (lab_test_id and client_id):
            return Response(
                {
                    "error": "Both lab_test_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        lab_test = self.get_lab_test(client_id, lab_test_id)
        if not lab_test:
            return Response(
                {"error": "Lab test not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = LabTestUpdateSerializer(lab_test, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Lab test updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ClientLabTestDeleteByIDView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        lab_test_id = data.get("lab_test_id")

        if not (lab_test_id and client_id):
            return Response(
                {
                    "error": "Both lab_test_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            lab_test = LabTest.objects.get(client_id=client_id, lab_test_id=lab_test_id)
            lab_test.delete()
            return Response(
                {"message": "Lab test deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except LabTest.DoesNotExist:
            return Response(
                {"error": "Lab test not found"}, status=status.HTTP_404_NOT_FOUND
            )
