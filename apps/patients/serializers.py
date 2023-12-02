from rest_framework import serializers
import re
from apps.patients.models import Patient


# for pateint Register
class PatientRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "gender",
            "email",
            "contact_number",
            "address",
            "date_of_birth",
            "medical_history",
            "client",
        
        ]

# for Pateint Listing....
class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields ="__all__"


# for Pateint Listing By id....
class PatientListIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


# for Pateint updatePr0file put/patch By id....
class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "gender",
            "email",
            "contact_number",
            "address",
            "date_of_birth",
            "medical_history",
            
        ]

    # update method..
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# -- for Pateint Profile Searching By Query.....
class PatientSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


# @get Toatl Count doctor api
class TotalPatientCountSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    total_count = serializers.IntegerField()



class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "patient_id",
            "first_name",
            "last_name",
            "gender",
            "email",
            "contact_number",
            "address",
            "date_of_birth",
            "medical_history",
            "created_at",
            "updated_at",
            "client_id",
        ]
        



#This api is for compaign Run...

class PatientCompaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "gender",
            "email",
            "address",
            "contact_number",
            "date_of_birth",
            "client", #hard code depends up on hospital id..
        ]
    def validate(self, data):
        email = data.get('email')
        contact_number = data.get('contact_number')

        if email:
            # Validate email format using a regular expression
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise serializers.ValidationError("Invalid email format.")

        if contact_number:
            # Validate phone number format using a regular expression
            if not re.match(r'^\+?[1-9]\d{1,14}$', contact_number):
                raise serializers.ValidationError("Invalid phone number format.")

        return data





  