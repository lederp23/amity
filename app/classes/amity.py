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
    changes = False

    def create_room(self, room_names):
        """creates new room"""
        room_lists = []
        for room in self.rooms:
            room_lists.append(room['room'])
        room_type = ""
        message = ""
        room_found = False
        for count in range(0, len(room_names)):
            if room_names[count] in room_lists:
                message = room_names[count] + " already exists"
            else:
                for new_room in self.new_rooms:
                    if room_names[count] == new_room['room']:
                        room_found = True
                if room_found:
                    message = message + "\n" + room_names[count] + " has already been added"
                else:
                    if count > 0:
                        if not room_names[count] in room_names[:count]:
                            message = message + "\n" + self.add_room(room_names[count])
                        else:
                            message = message + "\n" +room_names[count] + \
                                      " has already been added"
                    else:
                        message = message + "\n" + self.add_room(room_names[count])
        return message

    def add_room(self, room):
        """Creates a new room"""
        message = ""
        room_type = input("Enter room type for " +\
                          room + ":")
        if room_type.lower() == "office" or \
        room_type.lower() == "livingspace":
            self.new_rooms.append({'room': room,\
            'room_type': room_type.lower()})
            message = "Successfully added " + \
                      room
            self.changes = True
            return message
        else:
            return room + " can only be office or livingspace"

    def add_person(self, first_name, last_name, position, accomodation):
        """Adds person"""
        name = first_name + " " + last_name
        name = name.upper()
        found = False
        choice = "N"
        for person in self.people:
            if person['person'] == name:
                found = True
        if found:
            choice = input("A user already exists with such a name. " +\
                           "Enter 'Y' to proceed and 'N' to cancel.")
            choice = choice.upper()
            if choice == "Y":
                return self.add_person_now(first_name, last_name, position,\
                                    accomodation)
            elif choice == "N":
                return "Operation cancelled."
            else:
                return "Invalid choice. Can only be 'Y' or 'N'."
        else:
            return self.add_person_now(first_name, last_name, position, \
                accomodation)

    def add_person_now(self, first_name, last_name, position, accomodation):
        name = first_name + " " + last_name
        name = name.upper()
        username = first_name[0].upper() + last_name[0].upper() +\
                    str(len(self.people) + 1)
        if position == 'FELLOW' or position == 'STAFF':
            self.new_persons.append({'person': name, 'position': position,\
                                     'accomodate': accomodation,\
                                     'username': username})
            self.people.append({'person': name, 'position': position,\
                                'accomodate': accomodation,\
                                'username': username})
            print(self.allocate_person_office(username))
            if position == 'FELLOW' and accomodation == 'Y':
                print(self.allocate_person_livingspace(username))
            elif position == 'STAFF' and accomodation == 'Y':
                print("Staff cannot be allocated a livingspace")
            self.changes = True
            return "Successfully added " + name + " with username " + username
        else:
            return "Wrong input. Can only be FELLOW or STAFF"

    def reallocate(self, username, room):
        """Reassigns a person to a different room"""
        position = ""
        accomodate = "N"
        current_room = ""
        new_room = ""
        found = False
        room_found = False
        message = ""
        name_count = 0
        name = ''
        for persons in self.people:
            if persons['username'] == username:
                position = persons['position']
                accomodate = persons['accomodate']
                found = True
                person = persons['person']
        for guy in self.people:
            if guy['person'] == name:
                name_count += 1
        if found:
            for roomy in self.rooms:
                if not roomy['occupants'].find(person) == -1:
                    current_room = roomy['room']
            if not current_room == room:
                message = self.reallocate_person(room, current_room, person,\
                          room_found)
            else:
                if name_count > 1:
                    message = self.reallocate_person(room, current_room, person)
                else:
                    message = person + " has already been allocated to " + room
        else:
            message = "Person does not exist"
        return message

    def reallocate_person(self, room, current_room, person, room_found):
        message = ""
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
                        message = "Person had not been allocated a room"
                    break
                else:
                    message = room + " is full."
                break
        if not room_found:
            message = room + " does not exist."
        return message

    def print_allocations(self, option):
        """Prints a list of room allocations"""
        output = ""
        for room in self.rooms:
            if not room['occupants'] == "":
                output += "\n"
                output += (room['room'] + "\n" +\
                           ("-" * len(room['occupants'][1:])) + "\n")
                output += (room['occupants'][1:])
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
            if not assigned and person['position'] == 'FELLOW':
                output += ("\n" + person['person'])
        files = open(("unallocated" if option == None else option) + ".txt",\
                     "w")
        files.write(output)
        files.close()
        if output == "":
            return "No one is missing a room"
        else:
            return output

    def load_people(self):
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

    def allocate_person_office(self, username):
        """Allocates offices"""
        found = False
        name = ''
        for person in self.people:
            if person['username'] == username:
                found = True
                name = person['person']
        if found:
            if not username in self.allocated_office:
                room_number = randint(0, (len(self.offices)-1))
                current_room = self.offices[room_number]
                if len(self.offices_with_space) < 1:
                    return "There is no office with space"
                else:
                    if self.space[current_room['room']] > 0:
                        new_occupants = current_room['occupants'] + ',' + name
                        current_room['occupants'] = new_occupants
                        self.space[current_room['room']] -= 1
                        self.offices[room_number] = current_room
                        self.allocations.append({'room':current_room['room'],\
                                                 'occupant': name})
                        self.allocated_office.append(username)
                        self.changes = True
                        return "Successfully allocated " + name + " to " +\
                            current_room['room']
                    else:
                        try:
                            self.offices_with_space.remove(\
                                 current_room['room'])
                            self.allocate_person_office(username)
                        except ValueError:
                            self.allocate_person_office(username)
            else:
                return name + " has already been allocated an office."
        else:
            return "Person does not exist. Cannot allocate office."

    def allocate_person_livingspace(self, username):
        """Allocates living spaces"""
        name = ''
        found = False
        position = ""
        for person in self.people:
            if person['username'] == username:
                found = True
                position = person['position']
                name = person['person']
        if found:
            if not position == "STAFF":
                if not username in self.allocated_living:
                    room_number = randint(0, (len(self.livingspace)-1))
                    current_room = self.livingspace[room_number]
                    if len(self.livingspace_with_space) < 1:
                        return "There is no livingspace with space"
                    else:
                        if self.space[current_room['room']] > 0:
                            new_occupants = current_room['occupants'] + ',' +\
                                            name
                            current_room['occupants'] = new_occupants
                            self.space[current_room['room']] -= 1
                            self.livingspace[room_number] = current_room
                            self.allocations.append(\
                                 {'room': current_room['room'],\
                                  'occupant': name})
                            self.allocated_living.append(username)
                            self.changes = True
                            return "Successfully allocated " + name + \
                                " to "+ current_room['room']
                        else:
                            try:
                                self.livingspace_with_space.remove(\
                                    current_room['room'])
                                self.allocate_person_livingspace(username)
                            except ValueError:
                                self.allocate_person_livingspace(username)
                else:
                    return name + " has already been allocated a living space."
            else:
                return "Living spaces are for fellows only"
        else:
            return "Person does not exist. Cannot allocate living space."

    def reset(self):
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
        self.changes = False
        self.loaded = True

    def load_state(self, database):
        """Loads data from database"""
        self.reset()
        try:
            engine = create_engine("sqlite:///app/database/" + database + ".db")
            session = sessionmaker(bind=engine)
            new_session = session()
            database_rooms = new_session.query(RoomModel)
            database_people = new_session.query(PersonModel)
            people_list = database_people.all()
            for person in people_list:
                self.people.append({'person': person.name,\
                                    'position': person.position,\
                                    'accomodate': person.accomodate,\
                                    'username': person.username})
            room_list = database_rooms.all()
            for current_room in room_list:
                self.space.update({current_room.room_name: current_room.space})
                if current_room.room_type == 'office':
                    self.offices.append({'room': current_room.room_name,\
                                         'room_type': current_room.room_type,\
                                         'max': current_room.maximum_capacity,\
                                         'space': current_room.space,\
                                         'occupants': current_room.occuppants})
                    room_occuppants = current_room.occuppants.split(",")
                    for occupant in room_occuppants:
                        for person in self.people:
                            if person['person'] == occupant:
                                self.allocated_office.append(person['username'])
                    if int(current_room.space) > 0:
                        self.offices_with_space.append(current_room.room_name)
                else:
                    self.livingspace.append(\
                        {'room': current_room.room_name,\
                         'room_type': current_room.room_type,\
                         'max':current_room.maximum_capacity,\
                         'space': int(current_room.space),\
                         'occupants': current_room.occuppants})
                    room_occuppants = current_room.occuppants.split(",")
                    for occupant in room_occuppants:
                        for person in self.people:
                            if person['person'] == occupant:
                                self.allocated_living.append(person['username'])
                    if current_room.space > 0:
                        self.livingspace_with_space.append(\
                            current_room.room_name)
            self.rooms = self.offices + self.livingspace
            self.changes = False
            self.loaded = True
            return "Successfully loaded."
        except OperationalError:
            return database + " does not exist."

    def save_new_people(self, new_session):
        """"Adds new people to database"""
        for person in self.new_persons:
            if person['position'] == "FELLOW":
                new_fellow = Fellow(person['person'],\
                                    person['position'],\
                                    person['accomodate'],\
                                    person['username'])
                new_fellow.add(person['person'], person['username'], new_session)
                new_fellow.add_persons(person['person'],\
                                       person['position'],\
                                       person['accomodate'],\
                                       person['username'])
            else:
                new_staff = Staff(person['person'],\
                                  person['position'],\
                                  person['accomodate'],\
                                  person['username'])
                new_staff.add(person['person'], person['username'], new_session)
                new_staff.add_persons(person['person'],\
                                      person['position'],\
                                      person['accomodate'],\
                                      person['username'])

    def save_new_rooms(self, new_session):
        """Writes new rooms to database"""
        for room in self.new_rooms:
            if room['room_type'] == "office":
                new_room = Office(room['room'], room['room_type'])
                new_room.add(new_session)
            elif room['room_type'] == "livingspace":
                new_room = LivingSpace(room['room'], room['room_type'])
                new_room.add(new_session)

    def save_allocations(self, new_session):
        """Writes allocations to database"""
        for allocation in self.allocations:
            statement = update(RoomModel).\
            where(RoomModel.room_name == allocation['room']).\
            values({'occuppants': RoomModel.occuppants + "," + \
                                  allocation['occupant'], \
                    'space' : self.space[allocation['room']]})
            new_session.execute(statement)
            new_session.commit()

    def save_reallocations(self, new_session):
        """Writes reallocation changes to database"""
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
                RoomModel.room_name == person['current'])\
                .values({'occuppants': new_occupants_current,\
                         'space': self.space[current_room]})
            new_session.execute(statement)
            new_session.commit()
            statement = update(RoomModel).where(\
                        RoomModel.room_name == person['new'])\
                        .values({'occuppants': new_occupants_new,\
                                 'space': self.space[new_room]})
            new_session.execute(statement)
            new_session.commit()

    def update_rooms(self, new_session):
        """Updates room occupants"""
        for room in self.rooms:
            statement = update(RoomModel).where(\
                        RoomModel.room_name == room['room'])\
                        .values({'occuppants': room['occupants']})
            new_session.execute(statement)
            new_session.commit()

    def save_state(self, database):
        """Writes changes to database"""
        if self.changes:
            self.changes = False
            self.loaded = False
            engine = create_engine("sqlite:///app/database/" +\
                                  ("amity" if database == None else database)\
                                   + ".db")
            session = sessionmaker(bind=engine)
            new_session = session()
            Base.metadata.create_all(engine)
            self.save_new_people(new_session)
            self.save_new_rooms(new_session)
            self.save_allocations(new_session)
            self.save_reallocations(new_session)
            self.update_rooms(new_session)
            self.changes = False
            self.loaded = False
            return "Successfully saved."
        else:
            return "No changes have been made for saving."

    def print_room(self, room):
        """Prints list of people in room"""
        found = False
        people_list = ""
        people_list += ("-" * len(room) + "\n")
        people_list += (room + "\n")
        people_list += ("-" * len(room) + "\n")
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
