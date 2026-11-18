import datetime
from .room import Room
from .booking import Booking
# from booking import Booking


class PricingManager:
    @classmethod
    def calculate_price(cls, room:Room, players, booking_date) -> float:
        price = room.price_per_player * players
        if 5 <= players <= 6:
            price -= price * 10 / 100
        elif players >= 7:
            price -= price * 15 / 100

        # Friday is 4, Saturday is 5
        if booking_date.weekday() in [4,5]: 
            price += price * 15 / 100
        
        return round(price, 2)

    @classmethod
    def calculate_cancellation_fee(cls, booking:Booking, current_datetime) -> float:
        fee = 0
                
        if current_datetime + datetime.timedelta(hours=6) <= booking.get_datetime <= current_datetime + datetime.timedelta(hours=24):
            fee = booking.total_price * 25 / 100
        elif booking.get_datetime < current_datetime + datetime.timedelta(hours=6):
            fee = booking.total_price * 50 / 100

        return fee
