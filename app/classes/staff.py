"""Staff class module"""
from datetime import datetime
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.classes.person import Person
from app.models.models import *

class Staff(Person):
    """Class for staff"""
    livingroom = False

    def add(self, name, username, new_session):
        """Adds Staff to database"""
        staff = StaffModel(name=name, dateAdded=datetime.now(),\
                           username=username)
        new_session.add(staff)
        new_session.commit()
