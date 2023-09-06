from rest_framework import serializers
from doctors.models import Doctor


# Dr-Register-Serializer..
class DoctorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "first_name",
            "last_name",
            "profile_image",
            "gender",
            "email",
            "contact_number",
            "date_of_birth",
            "specialty",
            "qualifications",
            "address",
            "department",
            "client",
        ]

        def validate(self, attrs):
            email = attrs.get("email")
            if Doctor.objects.filter(email=email).exists():
                raise serializers.ValidationError("This email already exists.")
            return attrs

    def create(self, validated_data):
        return Doctor.objects.create(**validated_data)


# Dr-AllDetails-Serializer..


# class DoctorListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Doctor
#         fields = "__all__"


# update Doctor Details...
class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "first_name",
            "last_name",
            "profile_image",
            "gender",
            "email",
            "contact_number",
            "date_of_birth",
            "specialty",
            "qualifications",
            "address",
            "department",
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# dr-search by name query..
class DoctorSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


# @get Total Count doctor api
class TotalDoctorCountSerializer(serializers.Serializer):
    total_count = serializers.IntegerField()


# @filter serching by name and id
class FilterSearchNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "first_name",
            "last_name",
            "gender",
            "email",
            "contact_number",
            "date_of_birth",
            "specialty",
            "qualifications",
            "address",
            "department",
        ]


class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "doctor_id",
            "first_name",
            "last_name",
            "profile_image",
            "gender",
            "email",
            "contact_number",
            "date_of_birth",
            "specialty",
            "qualifications",
            "address",
            "department",
            "created_at",
            "updated_at",
            "client_id",
        ]
