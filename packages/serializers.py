from rest_framework import serializers
from .models import Package


class PackageCreateSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField()
    client = serializers.CharField()

    class Meta:
        model = Package
        fields = [
            "package_name",
            "client",
            "current_package",
            "description",
            "monthly_price",
            "yearly_price",
            "start_date",
            "end_date",
        ]

    def validate(self, data):
        package_name = data.get('package_name')
        package_id = data.get('package_id')
    
        # Check for duplicate entries
        if Package.objects.filter(package_name=package_name, package_id=package_id).exists():
            raise serializers.ValidationError("Package with the same package_id and client already exists.")

        # If there are no duplicates, return the data
        return data



class PackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"
