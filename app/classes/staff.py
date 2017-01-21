"""Staff class module"""
from datetime import datetime
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.classes.person import Person
from app.models.models import *

class Staff(Person):
    """Class for staff"""
    livingroom = False

    def add(self, name):
        """Adds Staff to database"""
        staff = StaffModel(name=name, dateAdded=datetime.now())
        session.add(staff)
        session.commit()

    def delete(self, names):
        """Deletes staff from database"""
        try:
            person = session.query(StaffModel).filter_by(name=names).first()
            session.delete(person)
            session.commit()
        except UnmappedInstanceError:
            pass
