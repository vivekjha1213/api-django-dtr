from rest_framework import serializers
from .models import Prescription

from patients.models import Patient  #  Patient model
from doctors.models import Doctor

class PrescriptionCreateSerializer(serializers.ModelSerializer):
    # Create separate fields for date and time
    prescription_date = serializers.DateField()
    prescription_time = serializers.TimeField()

    class Meta:
        model = Prescription
        fields = ["patient", "doctor", "prescription_date", "prescription_time", "notes", "client"]

    def validate(self, data):
        patient = data.get("patient")
        doctor = data.get("doctor")
        prescription_date = data.get("prescription_date")
        prescription_time = data.get("prescription_time")

        # Check if a prescription with the same patient, doctor, date, and time already exists
        existing_prescription = Prescription.objects.filter(
            patient=patient,
            doctor=doctor,
            prescription_date=prescription_date,
            prescription_time=prescription_time,
        ).first()

        if existing_prescription:
            raise serializers.ValidationError("Duplicate prescription not allowed.")

        return data

class PrescriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"

class PrescriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["patient", "doctor", "prescription_date", "prescription_time", "notes"]
