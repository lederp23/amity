"""Main class module"""
from random import randint
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, update
from sqlalchemy.exc import OperationalError

from app.classes.fellow import *
from app.classes.livingspace import *
from app.classes.office import *
from app.classes.person import *
from app.classes.room import *
from app.classes.staff import *
from app.models.models import *

class Amity:
    """Contains main functions"""
    loaded = False
    new_person_details = []
    new_rooms = []
    new_persons = []
    offices = []
    livingspace = []
    rooms = []
    people = []
    allocations = []
    allocated_office = []
    allocated_living = []
    offices_with_space = []
    livingspace_with_space = []
    space = {}
    reallocation = []
    reallocated_people = []
    deallocated_people = []
    changes = False

    def create_room(self, room_names):
        """creates new room"""
        room_lists = []
        for room in self.rooms:
            room_lists.append(room['room'])
        room_type = ""
        message = ""
        for count in range(0, len(room_names)):
            if room_names[count] in room_lists:
                message = room_names[count] + " already exists"
            else:
                room_type = input("Enter room type for " + room_names[count] +\
                                  ":")
                if room_type.lower() == "office" or \
                room_type.lower() == "livingspace":
                    self.new_rooms.append({'room': room_names[count],\
                    'room_type': room_type.lower()})
                    message = message + "\nSuccessfully added " + \
                              room_names[count]
                    self.changes = True
                else:
                    message = message + "\n" +room_names[count] + \
                              " can only be office or livingspace"
        return message

    def add_person(self, first_name, last_name, position, accomodation):
        """Adds person"""
        name = first_name + " " + last_name
        found = False
        for person in self.people:
            if person['person'] == name:
                found = True
        if found:
            return "Person already exists"
        else:
            if position == 'FELLOW':
                self.new_persons.append({'person': name, 'position': position,\
                                         'accomodate': accomodation})
                self.people.append({'person': name, 'position': position,\
                                    'accomodate': accomodation})
                self.changes = True
                return "Successfully added " + name
            elif position == 'STAFF':
                self.new_persons.append({'person': name, 'position': position,\
                                         'accomodate': "N"})
                self.people.append({'person': name, 'position': position,\
                                    'accomodate': accomodation})
                self.changes = True
                return "Successfully added " + name
            else:
                return "Wrong input. Can only be FELLOW or STAFF"

    def reallocate(self, first_name, last_name, room):
        """Reassigns a person to a different room"""
        position = ""
        accomodate = "N"
        current_room = ""
        new_room = ""
        found = False
        room_found = False
        message = ""
        person = first_name + " " + last_name
        for persons in self.people:
            if persons['person'] == person:
                position = persons['position']
                accomodate = persons['accomodate']
                found = True
        if found:
            for roomy in self.rooms:
                if not roomy['occupants'].find(person) == -1:
                    current_room = roomy['room']
            if not current_room == room:
                for roomy in self.rooms:
                    if roomy['room'] == room:
                        room_found = True
                        if self.space[roomy['room']] > 0:
                            try:
                                self.space[room] -= 1
                                self.space[current_room] += 1
                                self.reallocated_people.append(\
                                    {'current': current_room,\
                                     'new': room, 'person': person})
                                message = person + " has been reallocated to "\
                                          + room
                                self.changes = True
                            except KeyError:
                                return "Person had not been allocated a room"
                            break
                        else:
                            return room + " is full."
                        break
                if not room_found:
                    message = room + " does not exist."
            else:
                message = person + " has already been allocated to " + room
        else:
            message = "Person does not exist"
        return message

    def print_allocations(self, option):
        """Prints a list of room allocations"""
        output = ""
        for room in self.rooms:
            if not room['occupants'] == "":
                output += "\n"
                output += (room['room'] + "\n" +\
                           ("-" * len(room['occupants'][1:])) + "\n")
                output +=( room['occupants'][1:])
                output += "\n"
        files = open(("allocations" if option == None else option) + ".txt",\
                     "w")
        files.write(output)
        files.close()
        return output

    def print_unallocated(self, option):
        """Prints list of unallocated people"""
        output = ""
        assigned = False
        output += "------------------\n"
        output += "Unallocated office\n"
        output += "------------------"
        for person in self.people:
            assigned = False
            for office in self.offices:
                if not office['occupants'].find(person['person']) == -1:
                    assigned = True
                    break
            if not assigned:
                output += ("\n" + person['person'])
        assigned = False
        output += "\n-----------------------\n"
        output += "Unallocated livingspace\n"
        output += "-----------------------"
        for person in self.people:
            assigned = False
            for livingspace in self.livingspace:
                if not livingspace['occupants'].find(person['person']) == -1:
                    assigned = True
                    break
            if not assigned:
                output += ("\n" + person['person'])
        files = open(("unallocated" if option == None else option) + ".txt",\
                     "w")
        files.write(output)
        files.close()
        if output == "":
            return "No one is missing a room"
        else:
            return output

    def load(self):
        """Loads people from txt file"""
        accomodate = ""
        individual = []
        if self.loaded:
            try:
                names = open('names.txt', 'r')
                self.new_person_details = names.readlines()
                for person in self.new_person_details:
                    person.replace(r"\n", "")
                    individual = person.strip().split(" ")
                    name = individual[0] + " " + individual[1]
                    position = individual[2]
                    if len(individual) < 4:
                        accomodate = "N"
                    else:
                        accomodate = individual[3]
                    exists = False
                    for person in self.people:
                        if name == person['person']:
                            position = person['position']
                            accommodate = person['accomodate']
                            exists = True
                    if not exists:
                        print(self.add_person(name.split(" ")[0],\
                                              name.split(" ")[1],\
                                              position, accomodate))
                    else:
                        print(name + " has already been added.")
                return "Successfully loaded."
            except FileNotFoundError:
                return "names.txt not found."
        else:
            return "Load state first"

    def allocate_person_office(self, first_name, last_name):
        """Allocates offices"""
        found = False
        name = first_name + " " + last_name
        for person in self.people:
            if person['person'] == name:
                found = True
        if found:
            if not name in self.allocated_office:
                room_number = randint(0, (len(self.offices)-1))
                current_room = self.offices[room_number]
                if len(self.offices_with_space) < 1:
                        return "There is no office with space"
                else:
                    if self.space[current_room['room']] > 0:
                        new_occupants = current_room['occupants'] + name
                        current_room['occupants'] = new_occupants
                        self.space[current_room['room']] -= 1
                        self.offices[room_number] = current_room
                        self.allocations.append({'room':current_room['room'],\
                                                 'occupant': name})
                        self.allocated_office.append(name)
                        self.changes = True
                        return "Successfully allocated " + name + " to " +\
                            current_room['room']
                    else:
                        try:
                            self.offices_with_space.remove(\
                                 current_room['room'])
                            self.allocate_person_office(name)
                        except ValueError:
                            pass
            else:
                return name + " has already been allocated an office."
        else:
            return "Person does not exist. Cannot allocate office."

    def allocate_person_livingspace(self, first_name, last_name):
        """Allocates living spaces"""
        name = first_name + " " + last_name
        found = False
        position = ""
        for person in self.people:
            if person['person'] == name:
                found = True
                position = person['position']
        if found:
            if not position == "STAFF":
                if not name in self.allocated_living:
                    room_number = randint(0, (len(self.livingspace)-1))
                    current_room = self.livingspace[room_number]
                    if len(self.livingspace_with_space) < 1:
                        print("There is no livingspace with space")
                    else:
                        if self.space[current_room['room']] > 0:
                            new_occupants = current_room['occupants'] + name
                            current_room['occupants'] = new_occupants
                            self.space[current_room['room']] -= 1
                            self.livingspace[room_number] = current_room
                            self.allocations.append(\
                                 {'room': current_room['room'], 'occupant': name})
                            self.allocated_living.append(name)
                            self.changes = True
                            return "Successfully allocated " + name + \
                                " to "+ current_room['room']
                        else:
                            try:
                                self.livingspace_with_space.remove(\
                                    current_room['room'])
                                self.allocate_person_livingspace(name)
                            except ValueError:
                                pass
                else:
                    return name + " has already been allocated a living space."
            else:
                return "Living spaces are for fellows only"
        else:
            return "Person does not exist. Cannot allocate living space."


    def load_state(self, db):
        """Loads data from database"""
        self.new_person_details = []
        self.new_rooms = []
        self.new_persons = []
        self.offices = []
        self.livingspace = []
        self.rooms = []
        self.people = []
        self.allocations = []
        self.allocated_office = []
        self.allocated_living = []
        self.offices_with_space = []
        self.livingspace_with_space = []
        self.space = {}
        self.reallocation = []
        self.reallocated_people = []
        self.deallocated_people = []
        engine = create_engine(\
        "sqlite:///app/database/" \
        + db + ".db")
        session = sessionmaker(bind=engine)
        new_session = session()
        database_rooms = new_session.query(RoomModel)
        try:
            room_list = database_rooms.all()
            for current_room in room_list:
                self.space.update({current_room.room_name: current_room.space})
                if current_room.roomType == 'office':
                    self.offices.append({'room': current_room.room_name,\
                                         'room_type': current_room.roomType,\
                                         'max': current_room.maximum_capacity,\
                                         'space': current_room.space,\
                                         'occupants': current_room.occuppants})
                    room_occuppants = current_room.occuppants.split(",")
                    self.allocated_office += room_occuppants
                    if int(current_room.space) > 0:
                        self.offices_with_space.append(current_room.room_name)
                else:
                    self.livingspace.append(\
                        {'room': current_room.room_name,\
                         'room_type': current_room.roomType,\
                         'max':current_room.maximum_capacity,\
                         'space': int(current_room.space),\
                         'occupants': current_room.occuppants})
                    room_occuppants = current_room.occuppants.split(",")
                    for occupant in room_occuppants:
                        self.allocated_living.append(occupant)
                    if current_room.space > 0:
                        self.livingspace_with_space.append(\
                            current_room.room_name)
            database_people = new_session.query(PersonModel)
            people_list = database_people.all()
            for person in people_list:
                self.people.append({'person': person.name, 'position':\
                person.position, 'accomodate': person.accomodate})
            self.rooms = self.offices + self.livingspace
            self.changes = False
            self.loaded = True
            return "Successfully loaded."
        except OperationalError:
            return db + " does not exist."

    def save_state(self, db):
        """Writes changes to database"""
        if self.changes:
            self.changes = False
            self.loaded = False
            engine = create_engine(\
            "sqlite:///app/database/" \
            + ("amity" if db == None else db) + ".db")
            session = sessionmaker(bind=engine)
            new_session = session()
            Base.metadata.create_all(engine)
            for person in self.deallocated_people:
                current_room = ""
                new_occupants = ""
                for room in self.rooms:
                    if not room['occupants'].find(person['name']) == -1:
                        new_occupants = room['occupants'].replace(\
                                        ("," + person['name']), "")
                        current_room = room['room']
                statement = update(RoomModel).\
                            where(RoomModel.room_name == current_room).\
                            values({'occuppants': new_occupants,\
                                    'space': self.space[current_room]})
                new_session.execute(statement)
                new_session.commit()
            for person in self.new_persons:
                if person['position'] == "FELLOW":
                    new_fellow = Fellow(person['person'],\
                                        person['position'],\
                                        person['accomodate'])
                    new_fellow.add(person['person'])
                    new_fellow.add_persons(person['person'],\
                                           person['position'],\
                                           person['accomodate'])
                else:
                    new_staff = Staff(person['person'],\
                                      person['position'],\
                                      person['accomodate' ])
                    new_staff.add(person['person'])
                    new_staff.add_persons(person['person'],\
                                          person['position'],\
                                          person['accomodate'])
            for room in self.new_rooms:
                if room['room_type'] == "office":
                    new_room = Office(room['room'], room['room_type'])
                    new_room.add()
                elif room['room_type'] == "livingspace":
                    new_room = LivingSpace(room['room'], room['room_type'])
                    new_room.add()
            for allocation in self.allocations:
                statement = update(RoomModel).\
                where(RoomModel.room_name == allocation['room']).\
                values({'occuppants': RoomModel.occuppants + "," + \
                                      allocation['occupant'], \
                        'space' : self.space[allocation['room']]})
                new_session.execute(statement)
                new_session.commit()
            for person in self.reallocated_people:
                current_room = ""
                new_room = ""
                new_occupants_current = ""
                new_occupants_new = ""
                for room in self.rooms:
                    if room['room'] == person['current']:
                        new_occupants_current = room['occupants'].replace(\
                                                "," + person['person'], "")
                        current_room = room['room']
                        break
                for room in self.rooms:
                    if room['room'] == person['new']:
                        new_occupants_new = \
                            room['occupants'] + "," + person['person']
                        new_room = room['room']
                        break
                statement = update(RoomModel).where(\
                    RoomModel.room_name==person['current'])\
                    .values({'occuppants': new_occupants_current,\
                             'space': self.space[current_room]})
                new_session.execute(statement)
                new_session.commit()
                statement = update(RoomModel).where(\
                            RoomModel.room_name==person['new'])\
                            .values({'occuppants': new_occupants_new,\
                                     'space': self.space[new_room]})
                new_session.execute(statement)
                new_session.commit()
                self.changes = False
                self.loaded = False
            for room in self.rooms:
                statement = update(RoomModel).where(\
                            RoomModel.room_name==room['room'])\
                            .values({'occuppants': room['occupants']})
                new_session.execute(statement)
                new_session.commit()
            return "Successfully saved."
        else:
            return "No changes have been made for saving."

    def print_room(self, room):
        """Prints list of people in room"""
        found = False
        people_list = ""
        people_list += (room + "\n")
        for office in self.offices:
            if office['room'] == room:
                if len(office['occupants']) > 0:
                    people_list += (office['occupants'][1:].replace(",", "\n"))
                else:
                    people_list = room + " is empty."
                found = True
        for livingspace in self.livingspace:
            if livingspace['room'] == room:
                if len(livingspace['occupants']) > 0:
                    people_list += (livingspace['occupants'][1:].replace(\
                                    ",", "\n"))
                else:
                    people_list = room + " is empty."
                found = True
        if not found:
            return "Room not found"
        else:
            return people_list

    def deallocate_person(self, first_name, last_name, room_type):
        """Removes person from rooms"""
        exists = False
        name = first_name + " " + last_name
        found = False
        for person in self.people:
            if person['person'] == name:
                found = True
        if not found:
            return name + " does not exist"
        else:
            for room in self.rooms:
                if not room['occupants'].find(name) == -1:
                    exists = True
                    room['occupants'].replace(("," + name), "")
                    self.space[room['room']] += 1
                    self.deallocated_people.append({"name": name})
            if exists:
                if room_type == "office":
                    for room in self.offices:
                        if not room['occupants'].find(name) == -1:
                            room['occupants'].replace(("," + name), "")
                            self.changes = True
                            return "Successfully deallocated " + name
                elif room_type == "livingspace":
                    for room in self.livingspace:
                        if not room['occupants'].find(name) == -1:
                            room['occupants'].replace(("," + name), "")
                            self.changes = True
                            return "Successfully deallocated " + name
                else:
                    return "Wrong room type"
            else:
                return name + " has not been allocated"
