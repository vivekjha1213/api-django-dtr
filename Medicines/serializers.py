from rest_framework import serializers
from .models import Medicine

class MedicineRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = [
            "medicine_name",
            "manufacturer",
            "unit_price",
            "stock_quantity",
            "client",
        ]


class MedicineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields ="__all__"



class MedicineUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = [
            "medicine_name",
            "manufacturer",
            "unit_price",
            "stock_quantity",
        ]