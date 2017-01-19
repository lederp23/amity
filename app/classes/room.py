"""Room class module"""
import sys
class Room():
    """Class for rooms in Amity"""
    maximum_capacity = 0
    room =""
    roomType = ""
    occuppants = ""

    def __init__(self):
        """Creates a room"""

    def delete(self, name):
        """Deletes room from database"""
        deleted = session.query(RoomModel).filter_by(room_name=name).first()
        session.delete(deleted)
        session.commit()
