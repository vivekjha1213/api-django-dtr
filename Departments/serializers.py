from rest_framework import serializers
from .models import Department


class DepartmentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "client",
            "department_name",
        ]

    def validate(self, data):
        # Extract the client and department_name from the validated data
        client = data.get('client')
        department_name = data.get('department_name')

        # Check if a department with the same name already exists for the same client
        existing_department = Department.objects.filter(client=client, department_name=department_name).first()

        if existing_department:
            raise serializers.ValidationError("Department with the same name already exists for this client")

        return data


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"



class DepartmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "department_name",
        ]
    
    def validate_field1(self, value):
        # Perform validation for field1
        # For example, you can raise a validation error if the value is not within a certain range
        if value < 0:
            raise serializers.ValidationError("Field1 value must be non-negative")
        return value


class DepartmentSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
