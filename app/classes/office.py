"""Office class module"""
from app.classes.room import Room
from app.models.models import *

class Office(Room):
    """Class for offices"""
    def __init__(self, room, types):
        self.maximum_capacity = 6
        self.room = room
        self.roomType = types

    def add(self):
        """Adds room to database"""
        new_room = RoomModel(room_name = str(self.room), \
        roomType = str(self.roomType), maximum_capacity = int(\
        self.maximum_capacity), space = str(self.maximum_capacity), \
        occuppants = str(self.occuppants))
        session.add(new_room)
        session.commit()
