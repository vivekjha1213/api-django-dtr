from rest_framework import serializers
from .models import Package


class PackageCreateSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        package = Package.objects.create(**validated_data)
        return package

    def update(self, instance, validated_data):
        instance.package_name = validated_data.get(
            "package_name", instance.package_name
        )
        instance.client = validated_data.get("client", instance.client)
        instance.current_package = validated_data.get(
            "current_package", instance.current_package
        )
        instance.description = validated_data.get("description", instance.description)
        instance.monthly_price = validated_data.get(
            "monthly_price", instance.monthly_price
        )
        instance.yearly_price = validated_data.get(
            "yearly_price", instance.yearly_price
        )
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.save()
        return instance


class PackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            "package_id",
            "package_name",
            "current_package",
            "description",
            "monthly_price",
            "yearly_price",
            "start_date",
            "end_date",
            "client_id",
        ]
