from .room import Room, ROOM_OPENING_TIME, ROOM_CLOSING_TIME, ROOM_PREPERATION_TIME
from .booking import Booking
from .menu_manager import MenuManager
from .printer import Printer
from .room_manager import RoomManager
from .user_input import UserInput
from .parser import Parser

import datetime


class ReportManager:
    def __init__(self, rooms:list[Room], bookings:list[Booking], room_manager:RoomManager) -> None:
        self.rooms = rooms
        self.bookings = bookings
        self.room_manager = room_manager

        self.menu = MenuManager({
            1: ("Total Active Bookings", self.count_active_bookings),
            2: ("Total Inactive Bookings", self.count_cancelled_bookings),
            3: ("Total Rvnenue", self.calculate_total_revenue),
            4: ("Total Cancellation Fees", self.calculate_cancellation_revenue),
            5: ("The most booked room", self.get_most_popular_room),
            6: ("Number of bookings per room", self.get_room_booking_count),
            7: ("Room Occupancy Rate in Date", self.calculate_occupancy),
            8: ("Back to Main Menu", None)
            }, lambda: Printer.display_option_title("Reports Management"))


    def count_active_bookings(self):
        if not self.bookings:
            raise ValueError("There are no bookings in the system")
        
        counter = 0
        for b in self.bookings:
            if b.status == "Active":
                counter += 1
        print(counter)


    def count_cancelled_bookings(self):
        if not self.bookings:
            raise ValueError("There are no bookings in the system")
        
        counter = 0
        for b in self.bookings:
            if b.status == "Cancelled":
                counter += 1
        print(counter)


    def calculate_total_revenue(self):
        if not self.bookings:
            raise ValueError("There are no bookings in the system")
        
        total = sum(b.total_price for b in self.bookings if b.status == "Active")
        print(total)


    def calculate_cancellation_revenue(self):
        if not self.bookings:
            raise ValueError("There are no bookings in the system")
        
        total = sum(b.cancellation_fee for b in self.bookings)
        print(total)


    def get_booking_per_room(self, rooms = None):
        if not self.bookings:
            raise ValueError("There are no bookings in the system")
        
        rooms_instances = {}
        if rooms:
            for r in rooms:
                rooms_instances[r.room_id] = 0
        for b in self.bookings:
            rooms_instances[b.room_id] = rooms_instances.get(b.room_id, 0) + 1
        return rooms_instances


    def get_most_popular_room(self):
        rooms_instances = self.get_booking_per_room()
        most = max(rooms_instances, key=rooms_instances.get) # type: ignore
        print(f"{most} with {rooms_instances[most]} instances")
        

    def get_room_booking_count(self):
        rooms_instances = self.get_booking_per_room()
        print("Room ID".ljust(10), "Num of Bookings")
        print()
        for room_id, istances in rooms_instances.items():
            print(str(room_id).ljust(10), istances)


    def calculate_occupancy(self):
        if not self.bookings:
            raise ValueError("There are no bookings in the system")
        
        room = self.room_manager.search_room_by_id()
        date = UserInput.ask(Parser.parse_date, "Enter booking date [dd/mm/yyyy]: ")
        duration = datetime.timedelta(minutes = room.duration)
        preparation_time = datetime.timedelta(minutes = ROOM_PREPERATION_TIME)
        total_activity_time = datetime.timedelta(hours = ROOM_CLOSING_TIME - ROOM_OPENING_TIME)
        total_activity_utilization = datetime.timedelta()

        for b in self.bookings:
            if b.status == "Active" and b.room_id == room.room_id and b.booking_date == date:
                if b.get_datetime > b.get_datetime.replace(hour=ROOM_CLOSING_TIME):
                    total_activity_utilization += duration
                else:
                    total_activity_utilization += duration + preparation_time

        result = round(total_activity_utilization / total_activity_time * 100, 2)
        print(result, '%')
        

