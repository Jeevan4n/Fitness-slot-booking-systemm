from rest_framework import status, views
from rest_framework.response import Response
from .models import Class, Booking
from .serializers import ClassSerializer, BookingSerializer
from django.utils import timezone
from django.shortcuts import render

class BookClassView(views.APIView):
    def post(self, request):
        class_id = request.data.get('class_id')
        name = request.data.get('name')
        
        try:
            class_instance = Class.objects.get(pk=class_id)
            try:
                # Get the latest booking by id to generate a new user id
                latest_booking = Booking.objects.latest('id')
                next_user_id = latest_booking.id + 1
            except Booking.DoesNotExist:
                next_user_id = 1  # If no booking exists yet, start with id 1
        except Class.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Count the current number of bookings for the class
        booked_slots_count = Booking.objects.filter(class_instance=class_instance).count()
        
        if booked_slots_count < class_instance.capacity:
            Booking.objects.create(user_id=next_user_id, class_instance=class_instance, name=name)
            class_instance.booked_slots += 1
            class_instance.save()
            return Response({'message': 'Booking successful with Booking Id : '}, status=status.HTTP_200_OK)
        else:
            if next_user_id not in class_instance.waiting_list:
                class_instance.waiting_list.append(next_user_id)
                class_instance.save()
                return Response({'message': 'Added to waiting list'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User already in waiting list for this class'}, status=status.HTTP_400_BAD_REQUEST)

class CancelBookingView(views.APIView):
    def post(self, request):
        booking_id = request.data.get('booking_id')
        try:
            booking = Booking.objects.get(pk=booking_id)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        class_instance = booking.class_instance
        # Prevent cancellation if within 30 minutes of the class start
        if (class_instance.date - timezone.now()).total_seconds() <= 1800:
            return Response({'error': 'Cannot cancel within 30 minutes of the class'}, status=status.HTTP_400_BAD_REQUEST)

        booking.delete()
        class_instance.booked_slots -= 1

        # If there is a waiting list, move the first user from waiting list to booked slots
        if class_instance.waiting_list:
            next_user_id = class_instance.waiting_list.pop(0)
            Booking.objects.create(user_id=next_user_id, class_instance=class_instance)
            class_instance.booked_slots += 1

        class_instance.save()
        return Response({'message': 'Booking cancelled and waitlist updated'}, status=status.HTTP_200_OK)

class ClassListView(views.APIView):
    def get(self, request):
        filters = {}
        class_type = request.query_params.get('class_type')
        date = request.query_params.get('date')
        if class_type:
            filters['class_type'] = class_type
        if date:
            filters['date__date'] = date

        classes = Class.objects.filter(**filters)
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BookingDetailsView(views.APIView):
    def get(self, request):
        class_id = request.query_params.get('class_id')
        date = request.query_params.get('date')

        bookings = Booking.objects.all()
        if class_id:
            bookings = bookings.filter(class_instance__id=class_id)
        if date:
            bookings = bookings.filter(booked_at__date=date)

        if not bookings.exists():
            return Response({'message': 'No bookings found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
def index(request):
    # Renders the frontend's index page (adjust the path if needed)
    return render(request, 'frontend/build/index.html')
