import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import DestroyAPIView
from rest_framework import generics
from apps.Appointments.utils import Util
from apps.Hospitals.permissions import UnrestrictedPermission
from apps.Middleware.CustomPagination import PagePagination

from .models import Appointment
from .serializers import (
    AppointmentRegisterSerializer,
    CancelAppointmentSerializer,
    UpdateAppointmentSerializer,
)


# logger = logging.getLogger("Appointments.Appointment")

class AppointmentRegisterView(APIView):
    """
    API endpoint for registering an appointment.

    Accepts POST requests with appointment details.
    """
    def post(self, request, format=None):
        """
        Handle POST requests to register an appointment.

        Validates the appointment details and books the appointment if valid.

        Args:
            request: The HTTP request object.
            format: The format of the request data (default is None).

        Returns:
            Response: JSON response with success or error messages.
        """
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

            # send_doctor_appointment_confirmation.delay(doctor, appointment, patient, hospital)
            # send_patient_appointment_confirmation.delay(
            #     patient, appointment, doctor, hospital
            # )

            # Create a notification for the appointment booking

            return Response(
                {"message": "Appointment booked successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JoinListAppointmentView(generics.ListAPIView):
    """
    API endpoint to retrieve a list of appointments for a specific client.

    Supports GET and POST requests. For GET requests, it fetches a list of appointments for the provided client_id.
    """
    serializer_class = None
    pagination_class =PagePagination
    

    def get_queryset(self):
        """
        Retrieve the queryset for appointments with related patient and doctor information.

        Returns:
            queryset: Queryset containing appointment details.
        """
        
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
        """
        Handle POST requests to retrieve appointments for a specific client.

        Args:
            request: The HTTP request object containing client_id.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: List of appointments for the provided client_id or appropriate error response.
        """
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
    """
    API endpoint to count appointments for a client.
    """
    def post(self, request):
        """
        Count appointments for a specific client.

        Parameters:
        - request (Request): Django request object containing data.

        Returns:
        - Response: JSON response containing the total count of appointments for the client.
        """
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


class ClientDeleteAppointmentView(DestroyAPIView):
    """
    API endpoint to delete a client's appointment.
    """
    queryset = Appointment.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Delete a specific appointment for a client.

        Parameters:
        - request (Request): Django request object containing data.
        - args: Variable-length argument list.
        - kwargs: Arbitrary keyword arguments.

        Returns:
        - Response: JSON response confirming the success or failure of the deletion process.
        """
        
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

class ClientCancelAppointmentView(APIView):
    """
    API endpoint to cancel a client's appointment.
    """
    def put(self, request):
        """
        Cancel a specific appointment for a client.

        Parameters:
        - request (Request): Django request object containing data.

        Returns:
        - Response: JSON response confirming the success or failure of the cancellation process.
        """
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



class ClientAppointmentUpdateView(APIView):
    """
    API endpoint to update a client's appointment.
    """
    def update_appointment(self, appointment, data):
        """
        Helper method to update and reschedule an appointment.

        Parameters:
        - appointment (Appointment): Appointment instance to update.
        - data (dict): Data containing the updated appointment information.

        Returns:
        - Response: JSON response indicating the success or failure of the update.
        """
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
        """
        Update and reschedule an appointment using PUT method.

        Parameters:
        - request (Request): Django request object containing data.
        - args (list): Additional positional arguments.
        - kwargs (dict): Additional keyword arguments.

        Returns:
        - Response: JSON response confirming the success or failure of the update.
        """
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
        """
        Update and reschedule an appointment using PATCH method.

        Parameters:
        - request (Request): Django request object containing data.
        - args (list): Additional positional arguments.
        - kwargs (dict): Additional keyword arguments.

        Returns:
        - Response: JSON response confirming the success or failure of the update.
        """
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


class AppointmentCompaign(APIView):
    """
    API endpoint to handle appointment booking for a campaign.
    """
    permission_classes = [UnrestrictedPermission]
    def post(self, request, format=None):
        """
        Create an appointment for a campaign.

        Parameters:
        - request (Request): Django request object containing appointment data.
        - format (str, optional): Format of the request data.

        Returns:
        - Response: JSON response confirming the success or failure of the appointment booking.
        """
        serializer = AppointmentRegisterSerializer(data=request.data)

        if serializer.is_valid():
            doctor = serializer.validated_data["doctor"]
            patient = serializer.validated_data["patient"]
            appointment_date = serializer.validated_data["appointment_date"]

          
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

            # send_doctor_appointment_confirmation.delay(doctor, appointment, patient, hospital)
            # send_patient_appointment_confirmation.delay(
            #     patient, appointment, doctor, hospital
            # )

            # Create a notification for the appointment booking

            return Response(
                {"message": "Appointment booked successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
