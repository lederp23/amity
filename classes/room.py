"""Room class module"""
from classes.amity import *

class Room(Amity):
    """Class for rooms in Amity"""
    maximum_capacity = 0
    room =""
    roomType = ""
    occuppants = ""

    def __init__(self):
        """Creates a room"""

