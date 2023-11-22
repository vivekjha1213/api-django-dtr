from rest_framework import serializers
from apps.Medicines.models import Medicine

from apps.Prescriptions.models import Prescription
from .models import PrescriptionDetail

class PrescriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionDetail
        fields = ["prescription", "medicine", "dosage", "frequency", "client"]

    def validate(self, data):
        # Check for duplicate prescription entries
        prescription = data.get("prescription")
        medicine = data.get("medicine")
        dosage = data.get("dosage")
        frequency = data.get("frequency")
        client = data.get("client")

        if PrescriptionDetail.objects.filter(
            prescription=prescription,
            medicine=medicine,
            dosage=dosage,
            frequency=frequency,
            client=client,
        ).exists():
            raise serializers.ValidationError("This prescription detail already exists.")

        return data


class PrescriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionDetail
        fields = ["prescription_detail_id","prescription_id", "medicine_id", "dosage", "frequency","client_id"]




class PrescriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionDetail
        fields = ["prescription", "medicine", "dosage", "frequency",]