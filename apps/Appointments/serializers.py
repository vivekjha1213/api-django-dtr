from rest_framework import serializers
from apps.Hospitals.models import Hospital

from apps.doctors.models import Doctor
from apps.patients.models import Patient
from .models import Appointment


class AppointmentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "client",
            "patient",
            "doctor",
            "appointment_date",
            "start_time",
            "end_time",
        ]



class AppointmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "appointment_id",
            "appointment_date",
            "start_time",
            "end_time",
            "patient_id",
            "doctor_id",
            "status",
            "created_at",
            "updated_at",
        ]


class CountBookingSerializer(serializers.ModelSerializer):
    total_count = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ("total_count",)

    def get_total_count(self, obj):
        return Appointment.objects.count()


class CancelAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = []  # Specify the fields you want to include in the serializer

    def update(self, instance, validated_data):
        instance.status = "cancelled"
        instance.save()
        return instance


class UpdateAppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.IntegerField(source="doctor_id")
    patient = serializers.IntegerField(source="patient_id")
    appointment_date = serializers.DateField()

    class Meta:
        model = Appointment
        fields = [
            "patient",
            "doctor",
            "appointment_date",
            "start_time",
            "end_time",
        ]

    def validate(self, attrs):
        doctor_id = attrs.get("doctor_id")
        patient_id = attrs.get("patient_id")

        # Check if doctor with the given ID exists
        if not Doctor.objects.filter(doctor_id=doctor_id).exists():
            raise serializers.ValidationError(
                "Doctor with the provided ID does not exist."
            )

        # Check if patient with the given ID exists
        if not Patient.objects.filter(patient_id=patient_id).exists():
            raise serializers.ValidationError(
                "Patient with the provided ID does not exist."
            )

        return attrs

    def update(self, instance, validated_data):
        instance.doctor_id = validated_data.get("doctor_id")
        instance.patient_id = validated_data.get("patient_id")
        instance.appointment_date = validated_data.get("appointment_date")

        if instance.status != "Scheduled":
            instance.status = "ReScheduled"

        instance.save()
        return instance  # Check if the appointment is being rescheduled



# delete Appointment
class deleteAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = []


#@ update by client id and and 
class ClientUpdateAppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.IntegerField(source="doctor_id")
    patient = serializers.IntegerField(source="patient_id")
    appointment_date = serializers.DateField()
    client = serializers.IntegerField(source="client_id")  # Add client field

    class Meta:
        model = Appointment
        fields = [
            "patient",
            "doctor",
            "appointment_date",
            "start_time",
            "end_time",
            "client",  # Include client field
        ]

    def validate(self, attrs):
        doctor_id = attrs.get("doctor_id")
        patient_id = attrs.get("patient_id")
        client_id = attrs.get("client_id")  # Get client_id from attrs

        # Check if doctor with the given ID exists
        if not Doctor.objects.filter(doctor_id=doctor_id).exists():
            raise serializers.ValidationError("Doctor with the provided ID does not exist.")

        # Check if patient with the given ID exists
        if not Patient.objects.filter(patient_id=patient_id).exists():
            raise serializers.ValidationError("Patient with the provided ID does not exist.")

        # Check if client with the given ID exists
        if not Hospital.objects.filter(client_id=client_id).exists():
            raise serializers.ValidationError("Client with the provided ID does not exist.")

        return attrs

    def update(self, instance, validated_data):
        instance.doctor_id = validated_data.get("doctor_id")
        instance.patient_id = validated_data.get("patient_id")
        instance.appointment_date = validated_data.get("appointment_date")
        instance.client_id = validated_data.get("client_id")  # Set client_id

        if instance.status != "Scheduled":
            instance.status = "ReScheduled"

        instance.save()
        return instance




class CompaignBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "client",
            "patient",
            "doctor",
            "appointment_date",
            "start_time",
            "end_time",
        ]