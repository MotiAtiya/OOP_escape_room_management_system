from .room import Room
from .booking import Booking

class ReportManager:
    def __init__(self, rooms:list[Room], bookings:list[Booking]) -> None:
        self.rooms = rooms
        self.bookings = bookings
        
    def count_active_bookings(self):
        pass

    def count_cancelled_bookings(self):
        pass

    def calculate_total_revenue(self):
        pass

    def calculate_cancellation_revenue(self):
        pass

    def get_most_popular_room(self):
        pass

    def get_room_booking_count(self):
        pass

    def calculate_occupancy(self):
        pass

