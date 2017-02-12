"""Person class module"""
from datetime import datetime
from sqlalchemy.orm.exc import UnmappedInstanceError
from app.models.models import *

class Person():
    """Class for person"""
    name = ''
    role = ''
    accomodate = ''

    def __init__(self, names, person_role, accomodation, user_id):
        """Creates new person upon creating Person object"""
        self.name = names
        self.role = person_role
        self.accomodate = accomodation
        if accomodation == '' or accomodation == 'N':
            self.accomodate = False
        elif accomodation == 'Y':
            self.accomodate = True

    def add_persons(self, names, person_role, accomodation, user_id, new_session):
        """Adds person to database"""
        if accomodation == "":
            accomodation = "N"
        person = PersonModel(name=names, role=person_role,\
                             accomodate=accomodation,\
                             dateAdded=datetime.now(),\
                             user_id=user_id)
        new_session.add(person)
        new_session.commit()
