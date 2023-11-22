from rest_framework import serializers
from .models import Bed


class BedRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = [
            "client",
            "department",
            "is_occupied",
        ]

    def validate(self, data):
        # Check for duplicate entry based on client and department
        client = data.get("client")
        department = data.get("department")

        if Bed.objects.filter(client=client, department=department).exists():
            raise serializers.ValidationError(
                "A bed for this client and department already exists."
            )

        return data


class BedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = [
            "bed_id",
            "bed_number",
            "is_occupied",
            "created_at",
            "updated_at",
            "department_id",
            "client_id",
            "patient",
        ]


class BedUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = [
            "is_occupied",
            "bed_number",
        ]

    def validate_bed_number(self, value):
        bed_id = self.instance.bed_id if self.instance else None
        existing_bed = (
            Bed.objects.filter(bed_number=value).exclude(bed_id=bed_id).first()
        )

        if existing_bed:
            raise serializers.ValidationError(
                "Bed with this bed number already exists."
            )
        return value


class AvailableBedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = [
            "bed_id",
            "bed_number",
            "is_occupied",
           
        ]


class BedAssignPatientSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField()  # Add this field

    class Meta:
        model = Bed
        fields = ['patient_id', 'is_occupied']

    def update(self, instance, validated_data):
        patient_id = validated_data.pop('patient_id')
        instance.patient_id = patient_id  # Assign the patient ID
        instance.is_occupied = True
        instance.save()
        return instance
    
    
