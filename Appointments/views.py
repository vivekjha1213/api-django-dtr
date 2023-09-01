from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics
from .models import Appointment
from .serializers import (
    AppointmentListSerializer,
    AppointmentRegisterSerializer,
    CancelAppointmentSerializer,
    CountBookingSerializer,
    deleteAppointmentSerializer,
    UpdateAppointmentSerializer,
)


class AppointmentRegisterView(APIView):
    def post(self, request, format=None):
        serializer = AppointmentRegisterSerializer(data=request.data)

        if serializer.is_valid():
            doctor_id = serializer.validated_data["doctor"]
            patient_id = serializer.validated_data["patient"]
            appointment_date = serializer.validated_data["appointment_date"]

            # Check if the user has already booked an appointment with the same doctor on the same day
            if Appointment.objects.filter(
                doctor_id=doctor_id,
                patient_id=patient_id,
                appointment_date=appointment_date,  # Compare the entire datetime
            ).exists():
                return Response(
                    {"error": "Appointment already booked on the same day."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create the appointment and set status to "Scheduled"
            appointment = serializer.save(status="Scheduled")

            return Response(
                {"message": "Appointment booked successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentListView(APIView):
    def get(self, request, *args, **kwargs):
        appointments = Appointment.objects.all()
        serializer = AppointmentListSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# @get api  RetrieveAPIView its handle automatically....
class AppointmentListByIdView(RetrieveAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentListSerializer


# cancel apointment view.........
class CancelAppointmentView(APIView):
    def put(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(appointment_id=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {"success": False, "message": "Appointment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CancelAppointmentSerializer(
            instance=appointment, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Appointment successfully cancelled."}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Apointment view..........
class DeleteAppointmentView(DestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = deleteAppointmentSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Appointment delete successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


# Total Appointment booking.......
class CountBookingView(APIView):
    def get(self, request):
        serializer = CountBookingSerializer()
        total_count = serializer.get_total_count(None)
        return Response({"success": True, "total": total_count})


class AppointmentUpdateView(APIView):
    def put(self, request, *args, **kwargs):
        appointment_id = kwargs.get(
            "appointment_id"
        )  # Get the appointment ID from the URL
        try:
            appointment = Appointment.objects.get(appointment_id=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UpdateAppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            # Save the updated appointment
            updated_appointment = serializer.save()
            updated_appointment.status = "Rescheduled"  # Set status to "Rescheduled"
            updated_appointment.save()  # Save the status change

            return Response(
                {"message": "Appointment updated and rescheduled successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        appointment_id = kwargs.get(
            "appointment_id"
        )  # Get the appointment ID from the URL
        try:
            appointment = Appointment.objects.get(appointment_id=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UpdateAppointmentSerializer(
            appointment, data=request.data, partial=True
        )
        if serializer.is_valid():
            # Save the updated appointment
            updated_appointment = serializer.save()
            updated_appointment.status = "Rescheduled"  # Set status to "Rescheduled"
            updated_appointment.save()  # Save the status change

            return Response(
                {"message": "Appointment updated and rescheduled successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class JoinListAppointmentView(generics.ListAPIView):
#     serializer_class = None  # Set serializer_class to None

#     def get_queryset(self):
#         queryset = Appointment.objects.select_related("patient", "doctor").values(
#             "appointment_id",
#             "patient_id",  # Include patient_id
#             "patient__first_name",
#             "patient__last_name",
#             "doctor_id",  # Include doctor_id
#             "doctor__first_name",
#             "doctor__last_name",
#             "appointment_date",
#             "start_time",
#             "end_time",
#         )
#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()  # Call get_queryset to retrieve the queryset
#         data = list(queryset)
#         return Response(data)


# @ get all data by pasisinG, CLient-Id

class JoinListAppointmentView(generics.ListAPIView):
    serializer_class = None

    def get_queryset(self):
        queryset = Appointment.objects.select_related("patient", "doctor").values(
            "appointment_id",
            "patient_id",
            "patient__first_name",
            "patient__last_name",
            "doctor_id",
            "doctor__first_name",
            "doctor__last_name",
            "appointment_date",
            "start_time",
            "end_time",
            "status",
        )
        return queryset

    def post(self, request, *args, **kwargs):
        client_id = request.data.get("client_id")  # Get client_id from request data

        if client_id is not None:
            queryset = self.get_queryset().filter(client_id=client_id)
            data = list(queryset)

            if not data:
                return Response(
                    {"detail": f"No appointments found for client_id: {client_id}"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(data)

        return Response(
            {"detail": "No client_id provided in the request."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CountClientAppointmentView(APIView):
    def post(self, request):
        client_id = request.data.get("client_id")  # Get client_id from request data

        if client_id is not None:
            total_count = Appointment.objects.filter(client_id=client_id).count()
            return Response({"success": True, "total": total_count})
        else:
            return Response(
                {
                    "success": False,
                    "message": "client_id is required in the request data",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# @delete Appointment by clientId and Appointment Id .....
class ClientDeleteAppointmentView(DestroyAPIView):
    queryset = Appointment.objects.all()

    def post(self, request, *args, **kwargs):
        appointment_id = request.data.get("appointment_id")
        client_id = request.data.get("client_id")

        if appointment_id and client_id:
            try:
                appointment = Appointment.objects.get(
                    appointment_id=appointment_id, client_id=client_id
                )
                appointment.delete()
                return Response(
                    {"message": "Appointment deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except Appointment.DoesNotExist:
                return Response(
                    {"message": "Appointment not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {
                    "message": "Both appointment_id and client_id are required in the request data."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# @cancel Appontment by Appointment id and client id.................................
class ClientCancelAppointmentView(APIView):
    def put(self, request):
        appointment_id = request.data.get("appointment_id")
        client_id = request.data.get("client_id")

        if appointment_id and client_id:
            try:
                appointment = Appointment.objects.get(
                    appointment_id=appointment_id, client_id=client_id
                )
            except Appointment.DoesNotExist:
                return Response(
                    {"success": False, "message": "Appointment not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = CancelAppointmentSerializer(
                instance=appointment, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"success": True, "message": "Appointment successfully cancelled."}
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                    "success": False,
                    "message": "Both appointment_id and client_id are required in the request data.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# @ Update Appointment by client id and appointment Id
class ClientAppointmentUpdateView(APIView):
    def update_appointment(self, appointment, data):
        serializer = UpdateAppointmentSerializer(appointment, data=data, partial=True)
        if serializer.is_valid():
            updated_appointment = serializer.save()
            updated_appointment.status = "Rescheduled"  # Set status to "Rescheduled"
            updated_appointment.save()
            return Response(
                {"message": "Appointment updated and rescheduled successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        appointment_id = request.data.get("appointment_id")
        client_id = request.data.get("client_id")

        if appointment_id and client_id:
            try:
                appointment = Appointment.objects.get(
                    appointment_id=appointment_id, client_id=client_id
                )
            except Appointment.DoesNotExist:
                return Response(
                    {"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
                )
            return self.update_appointment(appointment, request.data)
        else:
            return Response(
                {
                    "error": "Both appointment_id and client_id are required in the request data."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, *args, **kwargs):
        appointment_id = request.data.get("appointment_id")
        client_id = request.data.get("client_id")

        if appointment_id and client_id:
            try:
                appointment = Appointment.objects.get(
                    appointment_id=appointment_id, client_id=client_id
                )
            except Appointment.DoesNotExist:
                return Response(
                    {"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
                )
            return self.update_appointment(appointment, request.data)
        else:
            return Response(
                {
                    "error": "Both appointment_id and client_id are required in the request data."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
            
    
