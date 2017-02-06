"""Staff class module"""
from datetime import datetime
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.classes.person import Person
from app.models.models import *

class Staff(Person):
    """Class for staff"""
    livingroom = False

    def add(self, name, username):
        """Adds Staff to database"""
        staff = StaffModel(name=name, dateAdded=datetime.now(),\
                           username=username)
        session.add(staff)
        session.commit()
