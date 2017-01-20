"""Person class module"""
from datetime import datetime
from sqlalchemy.orm.exc import UnmappedInstanceError
from app.models.models import *

class Person():
    """Class for person"""
    name = ''
    position = ''
    accomodate = ''

    def __init__(self, names, pos, accomodation):
        """Creates new person upon creating Person object"""
        self.name = names
        self.position = pos
        self.accomodate = accomodation
        if accomodation == '' or accomodation == 'N':
            self.accomodate = False
        elif accomodation == 'Y':
            self.accomodate = True

    def add_persons(self, names, pos, accomodation):
        """Adds person to database"""
        if accomodation == "":
            accomodation = "N"
        person = PersonModel(name = names, position = pos, \
        accomodate = accomodation, dateAdded = datetime.now())
        session.add(person)
        session.commit()

    def delete_persons(self, names):
        """Deletes person from database"""
        try:
            deleted = session.query(PersonModel).filter_by(name=names).first()
            session.delete(deleted)
            session.commit()
        except UnmappedInstanceError:
            pass
