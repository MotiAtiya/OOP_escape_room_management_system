from pathlib import Path
import json
from .room import Room
from .booking import Booking

class DataManager:
    def __init__(self):
        self.rooms_file = Path(__file__).parent.parent / "DATA/rooms.json"
        self.bookings_file = Path(__file__).parent.parent / "DATA/bookings.json"

    
    def __load_data(self, path) -> list:
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return []
        # except (UnicodeDecodeError, json.decoder.JSONDecodeError):
        #     raise

    def load_rooms(self):
        json_data = self.__load_data(self.rooms_file)
        data = []
        for d in json_data:
            data.append(Room.from_dict(d))
        return data

    
    def load_bookings(self):
        json_data = self.__load_data(self.bookings_file)
        data = []
        for d in json_data:
            data.append(Booking.from_dict(d))
        return data

    
    def __dump_data(self, path, data) -> None:
        json_data = []
        for d in data:
            json_data.append(d.to_dict())
        
        with open(path, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=2, ensure_ascii=False)

    
    def save_rooms(self, rooms):
        self.__dump_data(self.rooms_file, rooms)


    def save_bookings(self, bookings):
        self.__dump_data(self.bookings_file, bookings)

    