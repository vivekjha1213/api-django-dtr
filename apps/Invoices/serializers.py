from rest_framework import serializers

from .models import Invoice


class InvoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["patient", "invoice_date", "total_amount", "client"]

    def validate(self, data):
        patient = data.get("patient")
        invoice_date = data.get("invoice_date")

        # Check if an invoice with the same patient and invoice date already exists
        existing_invoice = Invoice.objects.filter(
            patient=patient, invoice_date=invoice_date
        ).exists()
        if existing_invoice:
            raise serializers.ValidationError(
                "An invoice with the same patient and invoice date already exists."
            )

        return data


class InvoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "invoice_id",
            "patient_id",
            "invoice_date",
            "total_amount",
            "created_at",
            "updated_at",
            "client_id",
        ]


class InvoiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["patient", "invoice_date", "total_amount"]
