from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Invoices.models import Invoice

from PrescriptionDetails.models import PrescriptionDetail

from .serializers import (
    InvoiceCreateSerializer,
    InvoiceListSerializer,
    InvoiceUpdateSerializer,
)


class InvoiceDetailsCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = InvoiceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Invoice added successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class ClientInvoiceDetailsListView(APIView):
    def post(self, request, *args, **kwargs):
        client_id = request.data.get(
            "client_id"
        )  # Get the client_id from the request data

        if not client_id:
            return Response(
                {"error": "client_id is required in the request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invoices = Invoice.objects.filter(client_id=client_id)

        if not invoices.exists():
            return Response(
                {"error": f"No invoices found for client with id {client_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = InvoiceListSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientInvoiceDetailsListByIdView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        invoice_id = data.get("invoice_id")

        if not (invoice_id and client_id):
            return Response(
                {
                    "error": "Both invoice_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            client_invoice = Invoice.objects.get(
                client_id=client_id, invoice_id=invoice_id
            )
        except Invoice.DoesNotExist:
            return Response(
                {"error": "No invoice found for the given criteria"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = InvoiceListSerializer(client_invoice)
        return Response({"Data": serializer.data})


# @get Toatl Count Invoice api by cliendID
class TotalInvoiceCountView(APIView):
    def post(self, request):
        client_id = request.data.get("client_id")  # Get client_id from request data

        if client_id is not None:
            total_count = Invoice.objects.filter(client_id=client_id).count()
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


    
    
    
    
class ClientInvoiceUpdateIDView(APIView):
    def get_Invoice(self, client_id, invoice_id):
        try:
            return Invoice.objects.get(client_id=client_id, invoice_id=invoice_id)
        except Invoice.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        invoice_id = data.get("invoice_id")

        if not (invoice_id and client_id):
            return Response(
                {
                    "error": "Both invoice_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        invoice = self.get_Invoice(client_id, invoice_id)
        if not invoice:
            return Response(
                {"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = InvoiceUpdateSerializer(invoice, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Invoice updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        invoice_id = data.get("invoice_id")

        if not (invoice_id and client_id):
            return Response(
                {
                    "error": "Both invoice_id and client_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        invoice = self.get_Invoice(client_id, invoice_id)
        if not invoice:
            return Response(
                {"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = InvoiceUpdateSerializer(invoice, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Invoice updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    

class ClientInvoiceDeleteByIDView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        invoice_id = data.get("invoice_id")
        
        if not (invoice_id and client_id):
            return Response({"error": "Both invoice_id and client_id are required in the request data"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            invoice = Invoice.objects.get(client_id=client_id, invoice_id=invoice_id)
            invoice.delete()
            return Response({"message": "Invoice deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)