"""Fellow class module"""
from sqlalchemy.orm.exc import UnmappedInstanceError
from datetime import datetime

from app.classes.person import Person
from app.models.models import *

class Fellow(Person):
    """Class for fellows"""
    name = ''
    livingroom = True


    def add(self, name, user_id, new_session):
        """Adds fellow to database"""
        fellow = FellowModel(name=name, dateAdded=datetime.now(),\
                             user_id=user_id)
        new_session.add(fellow)
        new_session.commit()
