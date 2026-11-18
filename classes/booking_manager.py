from .room import Room, ROOM_OPENING_TIME, ROOM_CLOSING_TIME, ROOM_PREPERATION_TIME
from .booking import Booking
from .pricing_manager import PricingManager
import datetime

class BookingManager:
    def __init__(self, rooms:list[Room], bookings:list[Booking]):
        self.rooms = rooms
        self.bookings = bookings
        self.pricing_manager = PricingManager

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

    def create_booking(self, customer_name, room_id, booking_date, start_time, players):
        room = list(filter(lambda r: r.room_id == room_id, self.rooms))[0]

        self.__validate_date(booking_date)
        self.__validate_room_opening_hours(start_time, room)
        self.check_availability(room_id, booking_date, start_time)

        booking_id = self.__get_next_booking_id()
        total_price = self.pricing_manager.calculate_price(room, players, booking_date)
        new_booking = Booking(booking_id, customer_name, room_id, booking_date, start_time, players, total_price)
        self.bookings.append(new_booking)
        # TODO save bookings

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

    def cancel_booking(self, booking_id, current_datetime):
        booking:Booking = self.get_booking(booking_id)
        if booking.status == "Cancelled":
            raise ValueError("This booking already cancelled before")
        if booking.get_datetime < current_datetime:
            raise ValueError("The order has already been redeemed. It cannot be cancelled")
        
        fee = self.pricing_manager.calculate_cancellation_fee(booking, current_datetime)


        booking.status = "Cancelled"
        booking.cancellation_fee = fee
        # TODO save bookings
