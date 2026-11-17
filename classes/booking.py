from dataclasses import dataclass
import datetime


@dataclass
class Booking:
    booking_id:str
    customer_name:str
    room_id:str
    booking_date:datetime.datetime
    start_time:str
    players:int
    total_price:float = 0
    status:str = "Active"
    cancellation_fee:float = 0

    # @property
    # def booking_date(self):
    #     return self.booking_date
    
    # @booking_date.setter
    # def booking_date(self, new_date):
    #     if isinstance(new_date, datetime.datetime):
    #         self.booking_date = new_date
    #     else:
    #         self.booking_date = datetime.datetime.strptime(new_date, "%Y-%m-%d")

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
            "start_time": self.start_time,
            "players": self.players,
            "total_price": self.total_price,
            "status": self.status,
            "cancellation_fee": self.cancellation_fee
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['booking_id'], data['customer_name'], data['room_id'], datetime.datetime.strptime(data['booking_date'], "%Y-%m-%d"),
                    data['start_time'], data['players'], data['total_price'], data['status'], data['cancellation_fee'])
