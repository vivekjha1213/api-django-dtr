from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Hospital  # Import your models

class HospitalTestCase(TestCase):
    def setUp(self):
        # Create a test hospital instance
        self.hospital = Hospital.objects.create(
            # Add relevant fields based on your model
            name="Test Hospital",
            email="test@example.com",
            # Add other fields as needed
        )
        self.client = APIClient()

    def test_hospital_list_view(self):
        # Ensure the hospital list view returns a 200 status code
        url = reverse("hospital-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hospital_detail_view(self):
        # Ensure the hospital detail view returns a 200 status code
        url = reverse("hospital-detail", args=[self.hospital.client_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hospital_registration_view(self):
        # Ensure the hospital registration view returns a 201 status code
        url = reverse("hospital-registration")
        data = {
            # Add relevant data for registration
            "name": "New Hospital",
            "email": "new@example.com",
            # Add other fields as needed
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_hospital_update_view(self):
        # Ensure the hospital update view returns a 200 status code
        url = reverse("hospital-update", args=[self.hospital.client_id])
        data = {
            # Add relevant data for update
            "name": "Updated Hospital",
            # Add other fields as needed
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hospital_delete_view(self):
        # Ensure the hospital delete view returns a 204 status code
        url = reverse("hospital-delete", args=[self.hospital.client_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
