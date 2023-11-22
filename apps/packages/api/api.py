from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from apps.Hospitals.permissions import UnrestrictedPermission
from ..models import Subscription
from ..serializers import PackageCreateSerializer, PackageListSerializer

class PackageCreateView(APIView):
    permission_classes = [UnrestrictedPermission]
    
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
    permission_classes=[UnrestrictedPermission]
    queryset = Subscription.objects.all()
    serializer_class = PackageListSerializer

class PackagedetailView(generics.ListAPIView):
    permission_classes=[UnrestrictedPermission]
    queryset=Subscription.objects.all()
    serializer_class=PackageListSerializer
    
    def get_queryset(self):
        package_id = self.request.query_params.get('package_id')
        if package_id:
            return Subscription.objects.filter(package_id=package_id)
        return Subscription.objects.none()


class PackageDeleteView(APIView):
    def post(self, request, package_id, format=None):
        try:
            package = Subscription.objects.get(package_id=package_id)
            package.delete()
            return Response(
                {"message": "Package deleted Successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Subscription.DoesNotExist:
            return Response(
                {"message": "Package not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
            
class PackageUpdateView(APIView):
    permission_classes = [UnrestrictedPermission]
    def put(self, request,package_id,format=None):
        
        try:
            package = Subscription.objects.get(package_id=package_id)
        except Subscription.DoesNotExist:
            return Response({"error": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PackageCreateSerializer(package, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Package updated Successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)