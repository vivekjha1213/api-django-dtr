import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import DestroyAPIView
from rest_framework import generics
from Appointments.utils import Util
from notifications.models import Notification


from .models import Appointment
from .serializers import (
    AppointmentRegisterSerializer,
    CancelAppointmentSerializer,
    UpdateAppointmentSerializer,
)

logger = logging.getLogger("Appointments.Appointment")


"""
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


"""



class AppointmentRegisterView(APIView):
    def post(self, request, format=None):
        serializer = AppointmentRegisterSerializer(data=request.data)

        if serializer.is_valid():
            doctor = serializer.validated_data["doctor"]
            patient = serializer.validated_data["patient"]
            appointment_date = serializer.validated_data["appointment_date"]

            # Check if the user has already booked an appointment with the same doctor on the same day
            if Appointment.objects.filter(
                doctor=doctor,
                patient=patient,
                appointment_date=appointment_date,  # Compare the entire datetime
            ).exists():
                return Response(
                    {"error": "Appointment already booked on the same day."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create the appointment and set status to "Scheduled"
            appointment = serializer.save(status="Scheduled")

            # Get hospital information (you need to implement this)
            hospital = appointment.client

            # Send confirmation emails to doctor and patient
            Util.send_doctor_appointment_confirmation(
                doctor, appointment, patient, hospital
            )
            Util.send_patient_appointment_confirmation(
                patient, appointment, doctor, hospital
            )
            
            
            # Create a notification for the appointment booking
            
            notification = Notification.objects.create(
                recipient=hospital,  # The hospital receives the notification
                notification_type='appointment_booking',  # Set the notification type
                message=f'Appointment booked for {patient} with {doctor} on {appointment_date}.',  
            )
            # Save the notification instance
            notification.save()
            
            return Response(
                {"message": "Appointment booked successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



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

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class CountClientAppointmentView(APIView):
    def post(self, request):
        client_id = request.data.get("client_id")  # Get client_id from request data

        if client_id is not None:
            total_count = Appointment.objects.filter(client_id=client_id).count()
            return Response({"success": True, "total_count": total_count})
        else:
            return Response(
                {
                    "success": False,
                    "message": "client_id is required in the request data",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#@cancel Appontment by Appointment id and client id.................................
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


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




