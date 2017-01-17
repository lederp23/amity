"""Fellow class module"""
import sys
from app.classes.person import Person
from app.models.models import *
from datetime import datetime

class Fellow(Person):
    """Class for fellows"""
    name = ''
    livingroom = True


    def add(self, name):
        """Adds fellow to database"""
        fellow = FellowModel(name = name, dateAdded = datetime.now())
        session.add(fellow)
        session.commit()
