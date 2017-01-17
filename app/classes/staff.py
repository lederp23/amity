"""Staff class module"""
from app.classes.person import Person
from app.models.models import *

from datetime import datetime
import sys
class Staff(Person):
    """Class for staff"""
    livingroom = False

    def add(self, name):
        """Adds Fellow to database"""
        staff = StaffModel(name = name, dateAdded = datetime.now())
        session.add(staff)
        session.commit()
