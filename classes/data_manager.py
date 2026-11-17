from pathlib import Path
import json
from .room import Room
from .booking import Booking

class DataManager:
    rooms_file = Path(__file__).parent.parent / "DATA/rooms.json"
    bookings_file = Path(__file__).parent.parent / "DATA/bookings.json"

    @staticmethod
    def __load_data(path) -> list:
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return []
        # except (UnicodeDecodeError, json.decoder.JSONDecodeError):
        #     raise

    @staticmethod
    def load_rooms():
        json_data = DataManager.__load_data(DataManager.rooms_file)
        data = []
        for d in json_data:
            data.append(Room.from_dict(d))
        return data

    @staticmethod
    def load_bookings():
        json_data = DataManager.__load_data(DataManager.bookings_file)
        data = []
        for d in json_data:
            data.append(Booking.from_dict(d))
        return data

    @staticmethod
    def __dump_data(path, data) -> None:
        json_data = []
        for d in data:
            json_data.append(d.to_dict())
        
        with open(path, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=2, ensure_ascii=False)

    @staticmethod
    def save_rooms(rooms):
        DataManager.__dump_data(DataManager.rooms_file, rooms)

    @staticmethod
    def save_bookings(bookings):
        DataManager.__dump_data(DataManager.bookings_file, bookings)

    