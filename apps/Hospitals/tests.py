from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Hospital

class HospitalLoginViewTest(TestCase):
     def setUp(self):
         self.client = APIClient()
         self.url = reverse('Login')  # Use the correct URL name "login"

         # Create a user using your custom Hospital model with a placeholder 'name'
         self.user = Hospital.objects.create_user(
             email='test@example.com',
             password='testpassword',
             name='Test User'  # Add a placeholder 'name' value
         )

     def test_hospital_login(self):
         data = {
             "email": "test@example.com",
             "password": "testpassword",
         }
         response = self.client.post(self.url, data, format='json')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertIn('access_token', response.data)
         self.assertIn('refresh_token', response.data)


class HospitalViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user for authentication (if needed)
        self.user = Hospital.objects.create_user(
            email='test@example.com',
            password='testpassword',
            name='Test User'
        )

        # Authenticate the client (if needed)
        self.client.force_authenticate(user=self.user)

        # Create some sample Hospital instances for testing
        self.hospital1 = Hospital.objects.create(
            client_id='123',
            hospital_name='Hospital A',
            name='John Doe',
            owner_name='Owner A',
            city='City A',
            address='Address A',
            email='hospital_a@example.com',
            phone='+1234567890',
            password='password_a',
            user_type='Admin'
        )

        self.hospital2 = Hospital.objects.create(
            client_id='124',
            hospital_name='Hospital B',
            name='Jane Doe',
            owner_name='Owner B',
            city='City B',
            address='Address B',
            email='hospital_b@example.com',
            phone='+9876543210',
            password='password_b',
            user_type='Doctor'
        )

    def test_hospital_update(self):
        url = reverse('hospital-update', args=[self.hospital1.client_id])
        data = {
            "name": "Updated Name",
            # Include other fields you want to update
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hospital_delete(self):
        url = reverse('hospital-retrieve-delete', args=[self.hospital2.client_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_hospital_list(self):
        url = reverse('hospital-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # You can also check if the response data matches your expected data

    def test_hospital_retrieve(self):
        url = reverse('list-By-id', args=[self.hospital1.client_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # You can also check if the response data matches your expected data

    def test_total_hospital_view(self):
        url = reverse('hospital-retrieve-total')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       