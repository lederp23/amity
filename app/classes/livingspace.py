"""LivingSpace class module"""
import sys
from app.classes.room import Room
from app.models.models import *

class LivingSpace(Room):
    """Class for livingrooms"""

    def __init__(self, room, types):
        """Sets maximum capacity"""
        self.maximum_capacity = 4
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
