from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models import Package
from ..serializers import PackageCreateSerializer, PackageListSerializer

class PackageCreateView(APIView):
    def post(self, request, format=None):
        
            serializer = PackageCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Package added Successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class PackageListView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer


class PackageDeleteView(APIView):
    def post(self, request, package_id, format=None):
        try:
            package = Package.objects.get(package_id=package_id)
            package.delete()
            return Response(
                {"message": "Package deleted Successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Package.DoesNotExist:
            return Response(
                {"message": "Package not found"},
                status=status.HTTP_404_NOT_FOUND,
            )