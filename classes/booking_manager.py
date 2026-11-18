from .room import Room, ROOM_OPENING_TIME, ROOM_CLOSING_TIME, ROOM_PREPERATION_TIME
from .booking import Booking
from .pricing_manager import PricingManager
from .menu_manager import MenuManager
from .user_input import UserInput
from .parser import Parser
from .room_manager import RoomManager
from .printer import Printer

import datetime

class BookingManager:
    def __init__(self, rooms:list[Room], bookings:list[Booking], room_manager:RoomManager):
        self.rooms = rooms
        self.bookings = bookings
        self.room_manager = room_manager
        self.pricing_manager = PricingManager

        self.menu = MenuManager({
            1: ("Create New Booking", self.add_booking),
            2: ("Display All Bookings", self.display_all_bookings),
            3: ("Search Booking", self.booking_details),
            4: ("Display Customer Bookings", self.customer_bookings),
            5: ("Display Bookings in Date", self.bookings_in_date),
            6: ("Change Booking Details", self.change_booking_details),
            7: ("Cancel Booking", self.cancel),
            8: ("Back to Main Menu", None)
        })

    def __get_next_booking_id(self):
        latest = max(self.bookings, key=lambda b: b.booking_id[1:])
        latest_id = int(latest.booking_id[1:])
        return 'B' + str(latest_id + 1).zfill(3)
    

    def __validate_date(self, booking_date):
        cureent_date = datetime.date.today()
        if cureent_date > booking_date:
            raise ValueError("Must be in the future")
        if booking_date > cureent_date.replace(year = cureent_date.year+1):
            raise ValueError("Date so far")


    def __validate_room_opening_hours(self, booking_start_time:datetime.time, room):
        start_day = datetime.time(hour=ROOM_OPENING_TIME)
        end_day = datetime.time(hour=ROOM_CLOSING_TIME)
        
        if booking_start_time < start_day:
            raise ValueError(f"The escape room is open from {start_day}")

        duration = datetime.timedelta(minutes = room.duration)
        booking_end_time = (datetime.datetime.combine(datetime.date.today(), booking_start_time) + duration).time()

        if booking_end_time > end_day:
            raise ValueError(f"The game must finish before {ROOM_CLOSING_TIME}:00 (the game takes {room.duration} minutes)")

    def check_availability(self, room_id, booking_date, start_time, exclude_booking_id=None):
        bookings_in_this_date = self.get_bookings_by_date(booking_date)
        if not bookings_in_this_date:
            return True

        room = list(filter(lambda r: r.room_id == room_id, self.rooms))[0]
        duration = datetime.timedelta(minutes = room.duration)
        preparation_time = datetime.timedelta(minutes = ROOM_PREPERATION_TIME)

        booking_datetime_start = datetime.datetime.combine(booking_date, start_time)
        booking_datetime_end = booking_datetime_start + duration + preparation_time

        for b in bookings_in_this_date:
            if exclude_booking_id and b.booking_id == exclude_booking_id:
                continue

            if b.room_id == room_id:
                existing_start = datetime.datetime.combine(b.booking_date, b.start_time)
                existing_end = existing_start + duration + preparation_time
                if booking_datetime_start < existing_end and booking_datetime_end > existing_start:
                    # raise ValueError("There is another booking at this time")
                    return False

    def create_booking(self, customer_name:str, room_id:str, booking_date:datetime.date, start_time:datetime.time, players:int):
        room = list(filter(lambda r: r.room_id == room_id, self.rooms))[0]

        self.__validate_date(booking_date)
        self.__validate_room_opening_hours(start_time, room)
        self.check_availability(room_id, booking_date, start_time)

        booking_id = self.__get_next_booking_id()
        total_price = self.pricing_manager.calculate_price(room, players, booking_date)
        new_booking = Booking(booking_id, customer_name, room_id, booking_date, start_time, players, total_price)
        self.bookings.append(new_booking)
        # TODO save bookings
        print(f"\nbooking {booking_id} added successfuly!")


    def add_booking(self):
        customer_name = UserInput.ask(Parser.parse_string, "Enter customer name: ")
        room = self.room_manager.search_room_by_id()
        if not room.is_active:
            raise ValueError("This room is inactive")

        date = UserInput.ask(Parser.parse_date, "Enter booking date [dd/mm/yyyy]: ")
        time = UserInput.ask(Parser.parse_time, "Enter booking time [hh:mm]: ")
        num_of_players = UserInput.ask(Parser.parse_from_range(room.min_players, room.max_players), "Enter num of players: ")
        self.create_booking(customer_name, room.room_id, date, time, num_of_players)


    def update_booking(self, booking_id, booking_date, start_time, players):
        booking = self.get_booking(booking_id)
        room = list(filter(lambda r: r.room_id == booking.room_id, self.rooms))[0]

        self.__validate_date(booking_date)
        self.__validate_room_opening_hours(start_time, room)
        self.check_availability(room.room_id, booking_date, start_time, booking_id)

        total_price = self.pricing_manager.calculate_price(room, players, booking_date)

        booking.booking_date = booking_date
        booking.start_time = start_time
        booking.players = players
        booking.total_price = total_price
        # TODO save bookings

    def change_booking_details(self):
        booking = self.search_booking_by_id()
        room = self.room_manager.get_room_by_id(booking.room_id)

        date = UserInput.edit(Parser.parse_date, "Enter booking date [dd/mm/yyyy]", booking.booking_date)
        time = UserInput.edit(Parser.parse_time, "Enter booking time [hh:mm]", booking.start_time)
        num_of_players = UserInput.edit(Parser.parse_from_range(room.min_players, room.max_players), "Enter num of players: ", booking.players)
        self.update_booking(booking.booking_id, date, time, num_of_players)


    def get_booking(self, booking_id) -> Booking:
        if not self.bookings:
            raise ValueError("There are no bookings in the system")

        return list(filter(lambda b: b.booking_id == booking_id, self.bookings))[0]

    def get_customer_bookings(self, customer_name):
        if not self.bookings:
            raise ValueError("There are no bookings in the system")

        return list(map(lambda b: b.customer_name.lower() == customer_name.lower(), self.bookings))
    
    
    def get_bookings_by_date(self, booking_date):
        if not self.bookings:
            raise ValueError("There are no bookings in the system")

        return list(filter(lambda b: b.booking_date == booking_date, self.bookings))



    def search_booking_by_id(self):
        if not self.bookings:
            raise ValueError("There are no bookings in the system")
        
        booking_id = UserInput.ask(Parser.parse_booking_id, "Enter booking ID: ")
        for b in self.bookings:
            if b.booking_id == booking_id:
                return b
        raise ValueError("Booking not found")


    def display_all_bookings(self):
        Printer.display_bookings(self.bookings)
        
    def booking_details(self):
        booking = self.search_booking_by_id()
        Printer.display_booking_details(booking)


    def search_bookings_by_customer_name(self):
        if not self.bookings:
            raise ValueError("There are no bookings in the system")
        
        customer_name = UserInput.ask(Parser.parse_string, "Enter customer name: ")
        result = []
        for b in self.bookings:
            if b.customer_name.lower() == customer_name.lower():
                result.append(b)
        if not result:
            raise ValueError("This customer name has not bookings")
        return result


    def customer_bookings(self):
        booking_list = self.search_bookings_by_customer_name()
        Printer.display_bookings(booking_list)


    def search_bookings_by_date(self):
        if not self.bookings:
            raise ValueError("There are no bookings in the system")
        
        date = UserInput.ask(Parser.parse_date, "Enter booking date [dd/mm/yyyy]: ")
        result = []
        for b in self.bookings:
            if b.booking_date == date:
                result.append(b)
        if not result:
            raise ValueError("There are not bookings in this date")
        return result


    def bookings_in_date(self):
        booking_list = self.search_bookings_by_date()
        Printer.display_bookings(booking_list)



    def cancel_booking(self, booking_id, current_datetime):
        booking:Booking = self.get_booking(booking_id)
        if booking.status == "Cancelled":
            raise ValueError("This booking already cancelled before")
        if booking.get_datetime < current_datetime:
            raise ValueError("The order has already been redeemed. It cannot be cancelled")
        
        fee = self.pricing_manager.calculate_cancellation_fee(booking, current_datetime)

        user_confirm = UserInput.ask(Parser.parse_yes_no_confirmation, f"Are you sure to cancel the booking? It will cost you a fee of {fee} [y/n]: ")
        if user_confirm == 'y':
            booking.status = "Cancelled"
            booking.cancellation_fee = fee
            # TODO save bookings
            print(f"\nBooking {booking_id} cancelled successfuly!")
        else:
            print(f"\nCancel cancelled!")



    def cancel(self):
        booking = self.search_booking_by_id()
        current_datetime = datetime.datetime.now()
        self.cancel_booking(booking.booking_id, current_datetime)
    


