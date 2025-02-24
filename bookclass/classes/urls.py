from django.urls import path
from .views import BookClassView, CancelBookingView, ClassListView, BookingDetailsView, index

urlpatterns = [
    path('book/', BookClassView.as_view(), name='book_class'),
    path('cancel/', CancelBookingView.as_view(), name='cancel_booking'),
    path('list/', ClassListView.as_view(), name='class_list'),
    path('booking-details/', BookingDetailsView.as_view(), name='booking_details'),
    path('', index, name='index'),
]
