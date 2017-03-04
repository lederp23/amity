"""Room class module"""
from app.models.models import *
from sqlalchemy.orm.exc import UnmappedInstanceError

class Room():
    """Class for rooms in Amity"""
    maximum_capacity = 0
    room =""
    room_type = ""
    occuppants = ""
