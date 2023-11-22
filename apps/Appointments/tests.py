from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from Hospitals.models import Hospital
from .models import Doctor, Patient, Appointment  


class AppointmentViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword", name="Test User"
        )
        self.client.force_authenticate(user=self.user)  # Authenticate the client

    def test_appointment_booking(self):
        # Create a hospital or client instance
        client = Hospital.objects.create(client_id=1)

        # Create a doctor and a patient with client_id
        doctor = Doctor.objects.create(client=client, first_name="Doctor Name")
        patient = Patient.objects.create(client=client, first_name="Patient Name")

        url = reverse("register-appointment")  # Replace with the actual URL name
        data = {
            "doctor": doctor.doctor_id,
            "patient": patient.patient_id,
            "appointment_date": "2023-09-20T14:00:00Z",  # Replace with a valid datetime
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.content)
        
        

        # Optionally, you can check if the appointment data matches your expectations
        self.assertEqual(response.data["doctor"], doctor.id)
        self.assertEqual(response.data["patient"], patient.id)
        self.assertEqual(response.data["appointment_date"], "2023-09-20T14:00:00Z")
       

        # You can also check if the appointment exists in the database
        appointment_exists = Appointment.objects.filter(
            doctor=doctor, patient=patient, appointment_date="2023-09-20T14:00:00Z"
        ).exists()
        self.assertTrue(appointment_exists)