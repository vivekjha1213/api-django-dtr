from rest_framework import serializers
from .models import Nurse


class NurseRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = [
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "contact_number",
            "department",
            "client",
        ]


class NurseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = "__all__"



class NurseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = [
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "contact_number",
            "department",
        ]