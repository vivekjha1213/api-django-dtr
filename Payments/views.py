from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment


from .serializers import (
    PaymentCreateSerializer,
    PaymentListSerializer,
    PaymentUpdateSerializer,
)


class PaymentDetailsCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Invoice added successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetailsListView(APIView):
    def get(self, request, *args, **kwargs):
        Payments = Payment.objects.all()
        serializer = PaymentListSerializer(Payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PaymentDetailsListByIdView(APIView):
    def get(self, request, pk, format=None):
        try:
            payment = Payment.objects.get(payment_id=pk)  # Retrieve a single instance
            serializer = PaymentListSerializer(payment)  # Serialize the single instance
            return Response(serializer.data[0], status=status.HTTP_200_OK)  # Return the serialized data without the brackets
        except PaymentUpdateSerializer.DoesNotExist:
            return Response(
                {"error": "Payment details not found"},
                status=status.HTTP_404_NOT_FOUND,
            )




class PaymentDetailsUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return None

    def put(self, request, pk, format=None):
        Payment = self.get_object(pk)
        if Payment is None:
            return Response(
                {"error": "Payment detail not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PaymentUpdateSerializer(Payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Payment detail updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        Payment = self.get_object(pk)
        if Payment is None:
            return Response(
                {"error": "Payment detail not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PaymentUpdateSerializer(Payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Payment detail updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return None

    def delete(self, request, pk, format=None):
        Payment = self.get_object(pk)
        if Payment is None:
            return Response(
                {"error": "Payment detail not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        Payment.delete()
        return Response(
            {"message": "Payment detail deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


# +++++++++++++++++++++++++++++++++++++++++++++++

class ClientPaymentDetailsListView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")

        if not client_id:
            return Response(
                {"error": "client_id is required in the request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payments = Payment.objects.filter(client_id=client_id)

        if not payments.exists():
            return Response(
                {"error": f"No nurses found for client with id {client_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PaymentListSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


'''

class ClientPaymentDetailsListByIdView(APIView):
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
            
            
            
            ''' 