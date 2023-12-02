from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Payment


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["invoice", "payment_date", "amount","client"]
        extra_kwargs = {
            "invoice": {
                "validators": [
                    UniqueValidator(queryset=Payment.objects.all(), message="Payment for this invoice already exists.")
                ]
            }
        }


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "payment_id",
            "invoice_id",
            "payment_date",
            "amount",
            "created_at",
            "updated_at",
            "client_id",
        ]


class  PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["invoice", "payment_date", "amount"]


