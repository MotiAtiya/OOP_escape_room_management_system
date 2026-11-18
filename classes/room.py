from dataclasses import dataclass

ROOM_OPENING_TIME = 10
ROOM_CLOSING_TIME = 22
ROOM_PREPERATION_TIME = 15

@dataclass
class Room:
    room_id:str
    name:str
    difficulty:str
    duration:int
    min_players:int
    max_players:int
    price_per_player:int
    is_active:bool = True

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def is_valid_players(self, players):
        return self.min_players <= players <= self.max_players

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "name": self.name,
            "difficulty": self.difficulty,
            "duration": self.duration,
            "min_players": self.min_players,
            "max_players": self.max_players,
            "price_per_player": self.price_per_player,
            "is_active": self.is_active
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['room_id'],
                   data['name'],
                   data['difficulty'],
                   data['duration'],
                   data['min_players'],
                   data['max_players'],
                   data['price_per_player'],
                   data['is_active'])
