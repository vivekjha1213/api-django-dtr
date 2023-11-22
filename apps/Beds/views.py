import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bed
from .serializers import (
    AvailableBedSerializer,
    BedAssignPatientSerializer,
    BedListSerializer,
    BedRegisterSerializer,
    BedUpdateSerializer,
)

logger = logging.getLogger("Beds.Bed")

class BedRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BedRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            bed_number = serializer.validated_data.get("bed_number")

            # Check if the bed is already occupied
            if Bed.objects.filter(bed_number=bed_number, is_occupied=True).exists():
                return Response(
                    {"error": "Bed is already occupied"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()  # Save the new bed record

            return Response(
                {"message": "Bed registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Get all Beds Data by client_id


def get_Bed_by_client_and_department(client_id, department_id):
    return Bed.objects.filter(
        department__client_id=client_id, department_id=department_id
    )


class ClienBedsListView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        department_id = data.get("department_id")

        if client_id and department_id:
            beds = get_Bed_by_client_and_department(client_id, department_id)

            if beds.exists():
                serializer = BedListSerializer(beds, many=True)
                return Response({"Data": serializer.data})
            else:
                return Response(
                    {
                        "error": "No beds found for the given client_id and department_id"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {
                    "error": "Both client_id and department_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# Get all Beds Data by client_id &  bed_id
class ClientBedListByIDView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        bed_id = data.get("bed_id")
        department_id = data.get("department_id")  # Add department_id

        if not (bed_id and client_id and department_id):  # Check for department_id
            return Response(
                {
                    "error": "Both bed_id, client_id, and department_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        beds = Bed.objects.filter(client_id=client_id)

        if bed_id:
            beds = beds.filter(bed_id=bed_id)  # Use the 'id' field to filter the bed

        if department_id:
            beds = beds.filter(
                department_id=department_id
            )  # Use the 'department_id' field to filter the bed

        if not beds.exists():
            return Response(
                {"error": "No bed found for the given criteria"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BedListSerializer(beds, many=True)
        return Response({"Data": serializer.data})


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# @get Total Count Beds api by cliendID
class TotalBedCountView(APIView):
    def post(self, request):
        client_id = request.data.get("client_id")  # Get client_id from request data

        if client_id is not None:
            total_count = Bed.objects.filter(client_id=client_id).count()
            return Response(
                {"success": True, "total_count": total_count}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "client_id is required in the request data",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Update Beds Data by client_id &  bed_id
class ClientBedUpdateView(APIView):
    def get_bed(self, client_id, department_id, bed_id):
        try:
            return Bed.objects.get(
                department__client_id=client_id, department_id=department_id, pk=bed_id
            )
        except Bed.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        department_id = data.get("department_id")
        bed_id = data.get("bed_id")

        bed = self.get_bed(client_id, department_id, bed_id)

        if not bed:
            return Response(
                {"error": "Bed not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BedUpdateSerializer(bed, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Bed updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        department_id = data.get("department_id")
        bed_id = data.get("bed_id")

        bed = self.get_bed(client_id, department_id, bed_id)

        if not bed:
            return Response(
                {"error": "Bed not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BedUpdateSerializer(bed, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Bed updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Delete Bed by clientID , DepartementId and bedId
class ClientBedDeleteByIDView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        department_id = data.get("department_id")
        bed_id = data.get("bed_id")

        if not (bed_id and client_id and department_id):
            return Response(
                {
                    "error": "bed_id, client_id, and department_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            bed = Bed.objects.get(
                client_id=client_id, department_id=department_id, bed_id=bed_id
            )
            bed.delete()
            return Response(
                {"message": "Bed deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Bed.DoesNotExist:
            return Response(
                {"error": "Bed not found"}, status=status.HTTP_404_NOT_FOUND
            )

    # Bed-Avail True or not  request


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class AvailableBedsView(APIView):
    def get_available_beds(self, client_id, department_id):
        return Bed.objects.filter(
            department__client_id=client_id,
            department_id=department_id,
            is_occupied=False,
        )

    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        department_id = data.get("department_id")

        if not (client_id and department_id):
            return Response(
                {
                    "error": "Both client_id and department_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        available_beds = self.get_available_beds(client_id, department_id)

        if available_beds.exists():
            serializer = AvailableBedSerializer(available_beds, many=True)
            return Response(
                {"message": "Available beds", "Data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "No available beds"}, status=status.HTTP_404_NOT_FOUND
            )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class BedAssignPatientView(APIView):
    def post(self, request, *args, **kwargs):
        client_id = request.query_params.get("client_id")
        department_id = request.query_params.get("department_id")
        bed_id = request.query_params.get("bed_id")

        if not (client_id and department_id and bed_id):
            return Response(
                {
                    "error": "client_id, department_id, and bed_id are required query parameters"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        bed = self.get_bed(client_id, department_id, bed_id)

        if not bed:
            return Response(
                {"error": "Bed not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BedAssignPatientSerializer(bed, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Patient assigned to bed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_bed(self, client_id, department_id, bed_id):
        try:
            return Bed.objects.get(
                department__client_id=client_id,
                department_id=department_id,
                bed_id=bed_id,
            )
        except Bed.DoesNotExist:
            return None

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class BedRemovePatientView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")
        department_id = data.get("department_id")
        bed_id = data.get("bed_id")

        if not (client_id and department_id and bed_id):
            return Response(
                {
                    "error": "client_id, department_id, and bed_id are required in the request data"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            bed = Bed.objects.get(
                department__client_id=client_id,
                department_id=department_id,
                bed_id=bed_id,
            )
        except Bed.DoesNotExist:
            return Response(
                {"error": "Bed not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if patient is present in the bed
        if bed.patient_id is None:
            return Response(
                {"error": "No patient found in the bed"},
                status=status.HTTP_404_NOT_FOUND,
            )

        bed.patient_id = None
        bed.is_occupied = False
        bed.save()

        return Response(
            {"message": "Patient removed from bed successfully"},
            status=status.HTTP_200_OK,
        )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def get_Bed_by_client(client_id):
    beds = Bed.objects.filter(client_id=client_id)
    return beds


class ClienBedsListByClientIdView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get("client_id")

        if client_id:
            beds = get_Bed_by_client(client_id)

            if beds.exists():
                serializer = BedListSerializer(beds, many=True)
                return Response({"Data": serializer.data})
            else:
                return Response(
                    {"error": "No beds found for the given client_id"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": "client_id is required in the request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++