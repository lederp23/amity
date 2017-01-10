"""Person class module"""
from models.models import *
from classes.amity import Amity
from datetime import datetime

class Person(Amity):
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

    def add_person(self, names, pos, accomodation):
        if accomodation == "":
            accomodation = "N"
        person = PersonModel(name = names, position = pos, accomodate = accomodation, dateAdded = datetime.now())
        session.add(person)
        session.commit()
