from .room import Room, ROOM_OPENING_TIME, ROOM_CLOSING_TIME, ROOM_PREPERATION_TIME
from .booking import Booking
from .pricing_manager import PricingManager
from .menu_manager import MenuManager
from .user_input import UserInput
from .parser import Parser
from .printer import Printer

class RoomManager:
    def __init__(self, rooms:list[Room]):
        self.rooms = rooms

        self.menu = MenuManager({
            1: ("Display All Rooms", self.display_rooms),
            2: ("Display Room Details", self.room_details),
            3: ("Add Room", self.add_room),
            4: ("Update Room", self.update_room),
            5: ("Active or Inactive Room", self.active_or_inactive_room),
            6: ("Back to Main Menu", None)
        })



    def display_rooms(self):
        Printer.display_rooms(self.rooms)


    def get_room_by_id(self, room_id):
        for r in self.rooms:
            if r.room_id == room_id:
                return r
        raise ValueError("Room not found")


    def search_room_by_id(self):
        # if not rooms:
        #     raise ValueError("There are no rooms in the system")
        room_id = UserInput.ask(Parser.parse_room_id, "Enter room ID: ")
        return self.get_room_by_id(room_id)


    def room_details(self):
        room = self.search_room_by_id()
        Printer.display_room_details(room)
        

    def get_next_room_id(self):
        latest = max(self.rooms, key=lambda r: r.room_id[1:])
        latest_id = int(latest.room_id[1:])
        return 'R' + str(latest_id + 1).zfill(3)


    def get_difficulty_description(self, val):
        difficulty = {
            1: "Easy",
            2: "Medium",
            3: "Hard"
        }
        if val in difficulty.values():
            return val
        return difficulty[val]


    def add_room(self):
        name = UserInput.ask(Parser.parse_string, "Enter room Name: ")
        difficulty = UserInput.ask(Parser.parse_from_range(1, 3), "Enter difficulty [1: Easey, 2: Medium, 3: Hard]: ")
        duration = UserInput.ask(Parser.parse_from_range(30, 120), "Enter game duration [from 30 min to 120 min]: ")
        min_players = UserInput.ask(Parser.parse_from_range(1, 10), "Enter minimum number of players [1-10]: ")
        max_players = UserInput.ask(Parser.parse_from_range(min_players, 40), f"Enter maximum number of players [{min_players}-40]: ")
        price_per_player = UserInput.ask(Parser.parse_positive_int_number, "Enter price per player: ")

        new_room = Room(self.get_next_room_id(),
                        name,
                        self.get_difficulty_description(difficulty),
                        duration,
                        min_players,
                        max_players,
                        price_per_player,
                        )
        
        self.rooms.append(new_room)
        # TODO save rooms
        print(f"\nroom {name} added successfuly!")


    def update_room(self):
        room = self.search_room_by_id()

        name = UserInput.edit(Parser.parse_string, "Enter room Name", room.name)
        difficulty = self.get_difficulty_description(UserInput.edit(Parser.parse_from_range(1, 3), "Enter difficulty [1: Easey, 2: Medium, 3: Hard]", room.difficulty))
        duration = UserInput.edit(Parser.parse_from_range(30, 120), "Enter game duration [from 30 min to 120 min]", room.duration)
        min_players = UserInput.edit(Parser.parse_from_range(1, 10), "Enter minimum number of players [1-10]", room.min_players)
        max_players = UserInput.edit(Parser.parse_from_range(min_players, 40), f"Enter maximum number of players [{min_players}-40]", room.max_players)
        price_per_player = UserInput.edit(Parser.parse_positive_int_number, "Enter price per player", room.price_per_player)

        room.name = name
        room.difficulty = difficulty
        room.duration = duration
        room.min_players = min_players
        room.max_players = max_players
        room.price_per_player = price_per_player

        # TODO save rooms
        print(f"\nroom {room.name} updated successfuly!")


    def active_or_inactive_room(self):
        room = self.search_room_by_id()
        status = room.is_active

        if status:
            msg = "The room is active now. Are you sure you want to inactive it? [y/n]: "
        else:
            msg = "The room is inactive now. Are you sure you want to active it? [y/n]: "
        
        user_confirm = UserInput.ask(Parser.parse_yes_no_confirmation, msg)
        if user_confirm == 'y':
            room.is_active = not room.is_active
            # TODO save rooms
            print(f"\nroom {room.name} updated successfuly!")
        else:
            print(f"\nUpdating cancelled!")



    # def run(self):
        # self.menu.run()
        # self.display_rooms()
