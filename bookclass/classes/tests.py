# classes/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Class, Booking

class BookingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_class = Class.objects.create(
            class_type='Yoga', 
            date='2024-09-01',
            capacity=10,
            booked_slots=0
        )
        self.test_user_id = 1

    def test_book_class(self):
        response = self.client.post('/api/book/', {'class_id': self.test_class.id, 'user_id': self.test_user_id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Booking successful')

    def test_cancel_booking(self):
        booking = Booking.objects.create(user_id=self.test_user_id, class_instance=self.test_class)
        response = self.client.post('/api/cancel/', {'booking_id': booking.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Booking cancelled and waitlist updated')
