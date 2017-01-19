"""Staff class module"""
from app.classes.person import Person
from app.models.models import *
from sqlalchemy.orm.exc import UnmappedInstanceError

from datetime import datetime
import sys

class Staff(Person):
    """Class for staff"""
    livingroom = False

    def add(self, name):
        """Adds Staff to database"""
        staff = StaffModel(name = name, dateAdded = datetime.now())
        session.add(staff)
        session.commit()

    def delete(self, names):
        """Deletes staff from database"""
        try:
            deleted = session.query(StaffModel).filter_by(name=names).first()
            session.delete(deleted)
            session.commit()
        except UnmappedInstanceError:
            pass
