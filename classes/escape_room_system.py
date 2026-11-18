from .room import Room
from .booking import Booking
from .data_manager import DataManager
from .booking_manager import BookingManager
from .room_manager import RoomManager
from .report_manager import ReportManager
from .menu_manager import MenuManager
from .printer import Printer


class EscapeRoomSystem:
    def __init__(self):
        self.data_manager = DataManager()
        self.rooms = self.data_manager.load_rooms()
        self.bookings = self.data_manager.load_bookings()
        self.room_manager = RoomManager(self.rooms, self.data_manager)
        self.booking_manager = BookingManager(self.rooms, self.bookings, self.room_manager, self.data_manager)
        self.report_manager = ReportManager(self.rooms, self.bookings, self.room_manager)


        self.menu = MenuManager({
            1: ("Rooms Management", self.room_manager.menu.run),
            2: ("Bookings Management", self.booking_manager.menu.run),
            3: ("Reports", self.report_manager.menu.run),
            4: ("Exit", None)
        }, lambda: Printer.display_system_title("ESCAPE ROOM MANAGEMENT SYSTEM"),
        False)


    def save_data(self):
        pass


    def run(self):
        self.menu.run()

