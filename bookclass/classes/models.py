from django.db import models
from django.utils import timezone

class Class(models.Model):
    YOGA = 'Yoga'
    GYM = 'Gym'
    DANCE = 'Dance'
    CLASS_TYPE_CHOICES = [
        (YOGA, 'Yoga'),
        (GYM, 'Gym'),
        (DANCE, 'Dance'),
    ]

    class_type = models.CharField(max_length=10, choices=CLASS_TYPE_CHOICES)
    date = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    booked_slots = models.PositiveIntegerField(default=0)
    waiting_list = models.JSONField(default=list)  # Stores user IDs in waiting list

    def __str__(self):
        return f"{self.class_type} class on {self.date.strftime('%Y-%m-%d %H:%M')}"




class Booking(models.Model):
    name = models.CharField(max_length=100, default="")  # Optional: store user's name
    user_id = models.CharField(max_length=100)  # Consider linking to a User model in production
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Booking {self.id} for {self.class_instance.class_type} by {self.name}"
