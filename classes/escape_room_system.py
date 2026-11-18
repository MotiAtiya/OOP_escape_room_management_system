from .room import Room
from .booking import Booking
from .data_manager import DataManager
from .booking_manager import BookingManager
from .report_manager import ReportManager
import datetime


class EscapeRoomSystem:
    def __init__(self):
        self.data_manager = DataManager()
        self.rooms = self.data_manager.load_rooms()
        self.bookings = self.data_manager.load_bookings()
        self.booking_manager = BookingManager(self.rooms, self.bookings)
        self.report_manager = ReportManager(self.rooms, self.bookings)

        # self.menu = {
        #     1: ("Rooms Management", lambda: rooms_management(rooms)),
        #     2: ("Bookings Management", lambda: bookings_management(rooms, bookings)),
        #     3: ("Reports", lambda: reports(rooms, bookings)),
        #     4: ("Exit", None)
        # }

    def save_data(self):
        pass


    def run(self):
        self.booking_manager.create_booking("mordechai", "R004", datetime.date(2026, 11, 18), datetime.time(14, 50), 6)
        
        print(self.bookings)

