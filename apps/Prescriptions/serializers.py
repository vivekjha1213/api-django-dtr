from rest_framework import serializers
from .models import Prescription

from apps.patients.models import Patient  #  Patient model
from apps.doctors.models import Doctor

class PrescriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["patient", "doctor", "prescription_date_time", "notes", "client"]

    def validate(self, data):
        patient = data.get("patient")
        doctor = data.get("doctor")
        prescription_date_time = data.get("prescription_date_time")
       

        # Check if a prescription with the same patient, doctor, date, and time already exists
        existing_prescription = Prescription.objects.filter(
            patient=patient,
            doctor=doctor,
            prescription_date_time=prescription_date_time,
            
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
        fields = ["patient", "doctor", "prescription_date_time", "notes"]
