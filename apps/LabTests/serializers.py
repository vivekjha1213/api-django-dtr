from rest_framework import serializers

from .models import LabTest


class LabTestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ["patient", "doctor", "test_name", "test_date", "results", "client"]

    def validate(self, data):
        patient = data.get("patient")
        doctor = data.get("doctor")
        test_name = data.get("test_name")

        # Check if a similar record already exists
        existing_records = LabTest.objects.filter(
            patient=patient, doctor=doctor, test_name=test_name
        )
        if existing_records.exists():
            raise serializers.ValidationError("A similar lab test already exists.")

        # Your other validation logic

        return data


class LabTestListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LabTest
        fields = [
           "lab_test_id",
            "patient_id",
            "doctor_id",
            "test_name",
            "test_date",
            "results",
            "created_at",
            "updated_at",
            "client_id",
        ]


class LabTestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ["patient", "doctor", "test_name", "test_date", "results"]

    # def validate(self, data):
    #     patient = data.get("patient")
    #     doctor = data.get("doctor")
    #     test_name = data.get("test_name")

    # Check if a similar record already exists
    #  existing_records = LabTest.objects.filter(patient=patient, doctor=doctor, test_name=test_name)
    #    if existing_records.exists():
    #     raise serializers.ValidationError("A similar lab test already exists.")

    # Your other validation logic

    # return data
