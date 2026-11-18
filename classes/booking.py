from dataclasses import dataclass
import datetime


@dataclass
class Booking:
    booking_id:str
    customer_name:str
    room_id:str
    booking_date:datetime.date
    start_time:datetime.time
    players:int
    total_price:float = 0
    status:str = "Active"
    cancellation_fee:float = 0

    def cancel(self, fee):
        self.status = "Cancelled"
        self.cancellation_fee = fee

    def update_details(self, booking_date, start_time, players, total_price):
        self.booking_date = booking_date
        self.start_time = start_time
        self.players = players
        self.total_price = total_price

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "customer_name": self.customer_name,
            "room_id": self.room_id,
            "booking_date": self.booking_date.strftime("%Y-%m-%d"),
            "start_time": self.start_time.strftime("%H:%M"),
            "players": self.players,
            "total_price": self.total_price,
            "status": self.status,
            "cancellation_fee": self.cancellation_fee
        }

    @property
    def get_datetime(self):
        return datetime.datetime.combine(self.booking_date, self.start_time)

    @classmethod
    def from_dict(cls, data):
        return cls(data['booking_id'],
                   data['customer_name'],
                   data['room_id'],
                   datetime.date.strptime(data['booking_date'], "%Y-%m-%d"),
                   datetime.time.strptime(data['start_time'], "%H:%M"),
                   data['players'],
                   data['total_price'],
                   data['status'],
                   data['cancellation_fee'])
