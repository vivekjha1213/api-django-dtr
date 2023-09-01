from rest_framework import serializers
from .models import Prescription

from patients.models import Patient  # Assuming you have a Patient model
from doctors.models import Doctor


class PrescriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["patient", "doctor", "prescription_date", "notes","client"]

    def validate(self, data):
        patient = data.get("patient")
        doctor = data.get("doctor")
        prescription_date = data.get("prescription_date")

        # Check if a prescription with the same patient, doctor, and date already exists
        existing_prescription = Prescription.objects.filter(
            patient=patient,
            doctor=doctor,
            prescription_date=prescription_date,
        ).first()

        if existing_prescription:
            raise serializers.ValidationError("Duplicate prescription not allowed.")

        return data


class PrescriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = [
            "prescription_id",
            "prescription_date",
            "notes",
            "patient_id",
            "patient_first_name",
            "patient_last_name",
            "doctor_id",
            "doctor_first_name",
            "doctor_last_name",
            "created_at",
            "updated_at",
            "client_id",
        ]


class PrescriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["patient", "doctor", "prescription_date", "notes","client"]
