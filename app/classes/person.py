"""Person class module"""
from app.models.models import *
from datetime import datetime
import sys
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
        if accomodation == "":
            accomodation = "N"
        person = PersonModel(name = names, position = pos, \
        accomodate = accomodation, dateAdded = datetime.now())
        session.add(person)
        session.commit()
