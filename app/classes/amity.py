"""Main class module"""
import shutil
import os
import sys
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
    default_db = "amity"
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
    space = {"":0}
    reallocation = []
    reallocated_people = []
    changes = False

    def create_room(self, room_names):
        """creates new room"""
        room_lists = []
        for room in self.rooms:
            room_lists.append(room['room'].upper())
        room_type = ""
        message = ""
        room_found = False
        for count in range(0, len(room_names)):
            if room_names[count].upper() in room_lists:
                message = room_names[count] + " already exists"
            else:
                for new_room in self.new_rooms:
                    if room_names[count] == new_room['room']:
                        room_found = True
                if room_found:
                    message = message + "\n" + room_names[count] +\
                              " has already been added"
                else:
                    if count > 0:
                        if not room_names[count] in room_names[:count]:
                            message = message + "\n" + \
                                      self.add_room(room_names[count])
                        else:
                            message = message + "\n" +room_names[count] + \
                                      " has already been added"
                    else:
                        message = message + "\n" + \
                                  self.add_room(room_names[count])
        return message

    def add_room(self, room):
        """Creates a new room"""
        message = ""
        room = room.upper()
        room_types = input("Enter room type for " +\
                          room + ":")
        room_type = room_types.lower()
        room_space = (6 if room_type == "office" else 4)
        if room_type.lower() == "office" or \
        room_type == "livingspace":
            self.new_rooms.append({'room': room.upper(),\
            'room_type': room_type})
            self.rooms.append({'room': room,\
                               'room_type': room_type,\
                               'max': room_space,\
                               'space': room_space,\
                               'occupants': ""})
            if room_type.lower() == "office":
                self.offices.append({'room': room,\
                                   'room_type': room_type,\
                                   'max': room_space,\
                                   'space': room_space,\
                                   'occupants': ""})
                self.offices_with_space.append(room)
            if room_type.lower() == "livingspace":
                self.livingspace.append({'room': room,\
                                   'room_type': room_type,\
                                   'max': room_space,\
                                   'space': room_space,\
                                   'occupants': ""})
                self.livingspace_with_space.append(room)
            self.space[room]= room_space
            message = "Successfully added " + \
                      room
            self.changes = True
            return message
        else:
            return room + " can only be office or livingspace"

    def add_person(self, first_name, last_name, role, accomodation):
        """Gets new person's details"""
        name = first_name + " " + last_name
        is_digit = any(char.isdigit() for char in name)
        if is_digit:
            return "Name cannot contain a digit"
        else:
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
                    return self.add_person_now(first_name, last_name, role,\
                                        accomodation)
                elif choice == "N":
                    return "Operation cancelled."
                else:
                    return "Invalid choice. Can only be 'Y' or 'N'."
            else:
                return self.add_person_now(first_name, last_name, role, \
                    accomodation)

    def add_person_now(self, first_name, last_name, role, accomodation):
        """Adds new person"""
        name = first_name + " " + last_name
        name = name.upper()
        user_id = first_name[0].upper() + last_name[0].upper() +\
                    str(len(self.people) + 1)
        if role == 'FELLOW' or role == 'STAFF':
            self.new_persons.append({'person': name, 'role': role,\
                                     'accomodate': accomodation,\
                                     'user_id': user_id})
            self.people.append({'person': name, 'role': role,\
                                'accomodate': accomodation,\
                                'user_id': user_id})
            print(self.allocate_person_office(user_id))
            if role == 'FELLOW' and (accomodation == 'Y' or accomodation == 'y'):
                print(self.allocate_person_livingspace(user_id))
            elif role == 'STAFF' and (accomodation == 'Y' or \
                 accomodation == 'y'):
                print("Staff cannot be allocated a livingspace")
            self.changes = True
            return "Successfully added " + name + " with user_id " + user_id
        else:
            return "Wrong input. Can only be FELLOW or STAFF"

    def reallocate(self, user_id, room):
        """Gets reallocation details"""
        role = ""
        accomodate = "N"
        current_rooms = []
        found = False
        room_found = False
        message = ""
        name_count = 0
        name = ''
        room_types = []
        room = room.upper()
        for persons in self.people:
            if persons['user_id'] == user_id:
                role = persons['role']
                accomodate = persons['accomodate']
                found = True
                name = persons['person']
        if found:
            for roomy in self.rooms:
                if name in roomy['occupants']:
                    current_rooms.append(roomy['room'])
                    room_types.append(roomy['room_type'])
            if not room in current_rooms:
                message = self.reallocate_person(room, current_rooms, name,\
                          room_found, room_types)
            else:
                message = name + " has already been allocated to " + room
        else:
            message = "Person does not exist"
        return message

    def reallocate_person(self, room, current_rooms, person, room_found,\
                          room_types):
        """Reallocates person"""
        message = ""
        current_room = ""
        current_room_index = 0
        new_room_type = ""
        for roomy in self.rooms:
            if room == roomy['room']:
                new_room_type = roomy['room_type']
        for roomy in self.rooms:
            if new_room_type == roomy['room_type'] and \
            roomy['room'] in current_rooms:
                current_room = roomy['room']
                current_room_index = self.rooms.index(roomy)
        for roomy in self.rooms:
            if roomy['room'] == room:
                room_found = True
                if not roomy['room_type'] in room_types:
                    message = "Reallocation cannot happen " +\
                              "with rooms of different types or if" + \
                              " a person had not been allocated a room."
                else:
                    if self.space[roomy['room']] > 0:
                        self.space[room] -= 1
                        self.space[current_room] += 1
                        self.reallocated_people.append(\
                            {'current': current_room,\
                             'new': room, 'person': person})
                        roomy['occupants'] += ("," + person)
                        self.rooms[current_room_index]['space'] = \
                        self.space[current_room]
                        roomy['space'] -= 1
                        self.rooms[current_room_index]['occupants'] = \
                        self.rooms[current_room_index]['occupants'].\
                        replace(("," + person), "")
                        message = person + " has been reallocated to "\
                                  + room
                        self.changes = True
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
        rooms_type = ""
        self.rooms = sorted(self.rooms, key=lambda k: k['room_type'])
        for room in self.rooms:
            if not room['occupants'] == "":
                if not room['room_type'] == rooms_type:
                    rooms_type = room['room_type']
                    output += ("\n" + ("*" * (len(rooms_type) + 1))+ "\n"  +\
                               rooms_type.upper() + "S\n" +\
                               ("*" * (len(rooms_type) + 1)))
                output += "\n"
                output += (room['room'] + "\n" +\
                           ("-" * len(room['occupants'][1:])) + "\n")
                output += (room['occupants'][1:])
                output += "\n"
        if output == "":
            return("There are no allocations.")
        else:
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
            if not assigned and person['role'] == 'FELLOW':
                output += ("\n" + person['person'])
        files = open(("unallocated" if option == None else option) + ".txt",\
                     "w")
        files.write(output)
        files.close()
        if output == "":
            return "No one is missing a room"
        else:
            return output

    def load_people(self, file_name):
        """Loads people from txt file"""
        accomodate = ""
        individual = []
        source = ('names' if file_name == None else file_name)
        try:
            names = open(source + '.txt', 'r')
            self.new_person_details = names.readlines()
            for person in self.new_person_details:
                person.replace(r"\n", "")
                individual = person.strip().split(" ")
                name = individual[0] + " " + individual[1]
                role = individual[2]
                if len(individual) < 4:
                    accomodate = "N"
                else:
                    accomodate = individual[3]
                exists = False
                for person in self.people:
                    if name == person['person']:
                        role = person['role']
                        accommodate = person['accomodate']
                        exists = True
                if not exists:
                    print(self.add_person(name.split(" ")[0],\
                                          name.split(" ")[1],\
                                          role, accomodate))
                else:
                    print(name + " has already been added.")
            return "Successfully loaded."
        except FileNotFoundError:
            return source + " not found."

    def allocate_person_office(self, user_id):
        """Allocates offices"""
        found = False
        name = ''
        for person in self.people:
            if person['user_id'] == user_id:
                found = True
                name = person['person']
        if found:
            if not user_id in self.allocated_office:
                try:
                    room_number = randint(0, (len(self.offices)-1))
                    current_room = self.offices[room_number]
                    if len(self.offices_with_space) < 1:
                        return "There is no office with space"
                    else:
                        if self.space[current_room['room']] > 0:
                            new_occupants = current_room['occupants'] + ',' + \
                                            name
                            current_room['occupants'] = new_occupants
                            self.space[current_room['room']] -= 1
                            self.offices[room_number] = current_room
                            self.allocations.append({'room':current_room['room'],\
                                                     'occupant': name})
                            self.allocated_office.append(user_id)
                            self.changes = True
                            for room in self.rooms:
                                if room['room'] == current_room['room']:
                                    room['occupants'] = new_occupants
                            return "Successfully allocated " + name + " to " +\
                                current_room['room']
                        else:
                            try:
                                self.offices_with_space.remove(\
                                     current_room['room'])
                            except ValueError:
                                pass
                            return self.allocate_person_office(user_id)
                except ValueError:
                    return "There is no office to allocate " + name
            else:
                return name + " has already been allocated an office."
        else:
            return "Person does not exist. Cannot allocate office."

    def allocate_person_livingspace(self, user_id):
        """Allocates living spaces"""
        name = ''
        found = False
        role = ""
        for person in self.people:
            if person['user_id'] == user_id:
                found = True
                role = person['role']
                name = person['person']
        if found:
            if not role == "STAFF":
                if not user_id in self.allocated_living:
                    try:
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
                                self.allocated_living.append(user_id)
                                self.changes = True
                                for room in self.rooms:
                                    if room['room'] == current_room['room']:
                                        room['occupants'] = new_occupants
                                return "Successfully allocated " + name + \
                                    " to "+ current_room['room']
                            else:
                                try:
                                    self.livingspace_with_space.remove(\
                                        current_room['room'])
                                    return self.allocate_person_livingspace(user_id)
                                except ValueError:
                                    return self.allocate_person_livingspace(user_id)
                    except ValueError:
                        return "There is no livingspace to allocate " + name
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
            self.default_db = database
            session = sessionmaker(bind=engine)
            new_session = session()
            database_rooms = new_session.query(RoomModel)
            database_people = new_session.query(PersonModel)
            people_list = database_people.all()
            for person in people_list:
                self.people.append({'person': person.name,\
                                    'role': person.role,\
                                    'accomodate': person.accomodate,\
                                    'user_id': person.user_id})
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
                                self.allocated_office.append(person['user_id'])
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
                                self.allocated_living.append(person['user_id'])
                    if current_room.space > 0:
                        self.livingspace_with_space.append(\
                            current_room.room_name)
            self.rooms = self.offices + self.livingspace
            self.changes = False
            self.loaded = True
            return "Successfully loaded."
        except OperationalError:
            os.remove("app/database/" + database + ".db")
            return database + " does not exist."

    def save_new_people(self, new_session):
        """"Adds new people to database"""
        self.new_persons = self.people
        for person in self.new_persons:
            if person['role'] == "FELLOW":
                new_fellow = Fellow(person['person'],\
                                    person['role'],\
                                    person['accomodate'],\
                                    person['user_id'])
                new_fellow.add(person['person'], person['user_id'], new_session)
                new_fellow.add_persons(person['person'],\
                                       person['role'],\
                                       person['accomodate'],\
                                       person['user_id'],
                                       new_session)
            else:
                new_staff = Staff(person['person'],\
                                  person['role'],\
                                  person['accomodate'],\
                                  person['user_id'])
                new_staff.add(person['person'], person['user_id'], new_session)
                new_staff.add_persons(person['person'],\
                                      person['role'],\
                                      person['accomodate'],\
                                      person['user_id'],
                                      new_session)

    def save_new_rooms(self, new_session):
        """Writes new rooms to database"""
        self.new_rooms = self.rooms
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

    def save_state(self, database):
        """Writes changes to database"""
        if self.changes:
            self.changes = False
            self.loaded = False
            try:
                os.remove("app/database/" + \
                        (database if database is not None else self.default_db)\
                        + ".db")
            except OSError:
                pass
            if not database == None:
                shutil.copy2(('app/database/default.db'), \
                             ('app/database/' + database + '.db'))
            exec(open("app/models/models.py").read())
            engine = create_engine("sqlite:///app/database/" +\
                                   (self.default_db if \
                                    database == None else database)\
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
        room = room.upper()
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

    def update_rooms(self, new_session):
        """Updates room occupants"""
        for room in self.rooms:
            statement = update(RoomModel).where(\
                        RoomModel.room_name == room['room'])\
                        .values({'occuppants': room['occupants']})
            new_session.execute(statement)
            new_session.commit()

    def show_user_id(self, name):
        """Shows the user_id of a person"""
        output = ""
        for person in self.people:
            if person['person'] == name.upper():
                output += (person['user_id'] + "\n")
        if output == "":
            return "Person not found"
        else:
            return output
