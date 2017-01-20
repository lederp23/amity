"""Fellow class module"""
from sqlalchemy.orm.exc import UnmappedInstanceError
from datetime import datetime

from app.classes.person import Person
from app.models.models import *

class Fellow(Person):
    """Class for fellows"""
    name = ''
    livingroom = True


    def add(self, name):
        """Adds fellow to database"""
        fellow = FellowModel(name = name, dateAdded = datetime.now())
        session.add(fellow)
        session.commit()

    def delete(self, names):
        """Deletes fellow from database"""
        try:
            deleted = session.query(FellowModel).filter_by(name=names).first()
            session.delete(deleted)
            session.commit()
        except UnmappedInstanceError:
            pass
