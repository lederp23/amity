"""Staff class module"""
from classes.person import Person
from models.models import *

from datetime import datetime

class Staff(Person):
    """Class for staff"""
    livingroom = False

    def add(self, name):
        """Adds Fellow to database"""
        staff = StaffModel(name = name, dateAdded = datetime.now())
        session.add(staff)
        session.commit()
