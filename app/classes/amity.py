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
    details = []
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
    reallocat = []
    changes = False

    def create_room(self, room):
        """creates new room"""
        room_lists = []
        for roomd in self.offices:
            room_lists.append(roomd['room'])
        for roomd in self.livingspace:
            room_lists.append(roomd['room'])
        types = ""
        msg = ""
        for count in range(0, len(room)):
            if room[count] in room_lists:
                msg = room[count] + " already exists"
            else:
                types = input("Enter room type for " + room[count] + ":")
                if types == "office" or types == "livingspace":
                    self.new_rooms.append({'room': room[count], 'types': types})
                    msg = msg + "\nSuccessfully added " + room[count]
                    self.changes = True
                else:
                    msg = "Room can only be office or livingspace"
        return msg

    def add_person(self, name, pos, accomodation):
        """Adds person"""
        if "_" in name:
            names = name.split("_")
            name = names[0] + " " + names[1]
        elif " " in name:
            pass
        else:
            return "Both first name and last name are required"
        found = False
        for guy in self.people:
            if guy['person'] == name:
                found = True
        if found:
            return "Person already exists"
        else:
            if pos == 'FELLOW':
                self.new_persons.append({'person': name, 'position': pos,\
                'accomodate': accomodation})
                self.people.append({'person': name, 'types': \
                    pos, 'accomodate': accomodation})
                return "Successfully added " + name
            elif pos == 'STAFF':
                self.new_persons.append({'person': name, 'position': pos,\
                'accomodate': accomodation})
                self.people.append({'person': name, 'types': \
                    pos, 'accomodate': accomodation})
                self.changes = True
                return "Successfully added " + name
            else:
                return "Wrong input. Can only be FELLOW or STAFF"

    def reallocate(self, person, room):
        """Reassigns a person to a different room"""
        pos = ""
        accomodate = "N"
        current_room = ""
        new_room = ""
        found = False
        msg = ""
        names = person.split("_")
        person = names[0] + " " + names[1]
        new_type = ""
        for persons in self.people:
            if persons['person'] == person:
                pos = persons['types']
                accomodate = persons['accomodate']
                found = True
        if found:
            for roomy in self.rooms:
                if person in roomy['occupants']:
                    current_room = roomy['room']
                    current_type = roomy['types']
                if roomy['room'] == room:
                    new_type = roomy['types']
            if not current_room == room:
                for roomy in self.rooms:
                    if roomy['room'] == room:
                        if self.space[roomy['room']] > 0:
                            self.reallocat.append({'current': current_room,\
                                            'new': room, 'person': person})
                            if current_type == new_type:
                                self.space[room] -= 1
                            self.space[current_room] += 1
                            msg = person + " has been reallocated to " + room
                            self.changes = True
                            break
                        else:
                            return room + " is full."
                        break
            else:
                msg = person + " has already been allocated to " + room
        else:
            msg = "Person does not exist"
        return msg

    def print_allocations(self, option):
        """Prints a list of room allocations"""
        output = ""
        roomm = ""
        self.allocations = sorted(self.allocations, key = lambda room:\
        (room['room'], room['occupant']))
        for alloc in self.allocations:
            if not roomm == alloc['room']:
                output += "\n\n"
                output += (alloc['room'] + "\n" + ("-" * 37) + "\n")
                roomm = alloc['room']
                output +=( alloc['occupant'])
            else:
                output +=(", " + alloc['occupant'])

            files = open(option + ".txt", "w")
            files.write(output)
            files.close()
        return output

    def print_unallocated(self, option):
        """Prints list of unallocated people"""
        unallocated = ""
        assigned = True
        for person in self.details:
            for alloc in self.allocations:
                if person in alloc['occupant']:
                    assigned = False
            if not assigned:
                unallocated += ("\n" + person)
        files = open(option + ".txt", "w")
        files.write(unallocated)
        files.close()
        if unallocated == "":
            return "No one is missing a room"
        else:
            return unallocated

    def load(self):
        """Loads people from txt file"""
        try:
            accomodate = ""
            individual = []
            try:
                names = open('names.txt', 'r')
                self.details = names.readlines()
                for person in self.details:
                    person.replace(r"\n", "")
                    individual = person.strip().split(" ")
                    name = individual[0] + " " + individual[1]
                    types = individual[2]
                    if len(individual) < 4:
                        accomodate = "N"
                    else:
                        accomodate = individual[3]
                    exists = False
                    accom = ""
                    for person in self.people:
                        if name == person['person']:
                            types = person['types']
                            accom = person['accomodate']
                            exists = True
                    if not exists:
                        print(self.add_person(name, types, accomodate))
                        print(self.allocate_person_office(name))
                        if types == "FELLOW":
                            if accomodate == "Y":
                                print(self.allocate_person_livingspace(name))
                    else:
                        print(name + " has already been added.")
                return "Successfully loaded."
            except FileNotFoundError:
                return "names.txt not found."
        except ValueError:
            return "Load state first before loading people."

    def allocate_person_office(self, name):
        """Allocates offices"""
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
                    self.allocations.append({'room':\
                    current_room['room'], 'occupant': name})
                    self.allocated_office.append(name)
                    self.changes = True
                    return "Successfully allocated " + name + " to " + \
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

    def allocate_person_livingspace(self, name):
        """Allocates living spaces"""
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
                    self.allocations.append({'room':\
                    current_room['room'], 'occupant': name})
                    self.allocated_living.append(name)
                    self.changes = True
                    return "Successfully allocated " + name + " to "\
                    + current_room['room']
                else:
                    try:
                        self.livingspace_with_space.remove(\
                            current_room['room'])
                        self.allocate_person_livingspace(name)
                    except ValueError:
                        pass
        else:
            return name + " has already been allocated a living space."

    def load_state(self, db):
        """Loads data from database"""
        self.allocations = []
        self.reallocat = []
        engine = create_engine(\
        "sqlite:////Users/olivermunala/Desktop/Amity/amity/app/database/" \
        + db + ".db")
        session = sessionmaker(bind=engine)
        new_session = session()
        con_room = new_session.query(RoomModel)
        try:
            room_list = con_room.all()
            for current_room in room_list:
                self.space.update({current_room.room_name: current_room.space})
                if current_room.roomType == 'office':
                    self.offices.append({'room': current_room.room_name,\
                    'types': current_room.roomType, 'max': \
                    current_room.maximum_capacity, 'space': \
                    current_room.space, 'occupants': \
                    current_room.occuppants})
                    allocatedd = current_room.occuppants.split(",")
                    self.allocated_office += allocatedd
                    if int(current_room.space) > 0:
                        self.offices_with_space.append(current_room.room_name)
                else:
                    self.livingspace.append({'room': current_room.room_name,\
                    'types': current_room.roomType, 'max': \
                    current_room.maximum_capacity, 'space': \
                    int(current_room.space), 'occupants': \
                    current_room.occuppants})
                    allocatedd = current_room.occuppants.split(",")
                    for acc in allocatedd:
                        self.allocated_living.append(acc)
                    if current_room.space > 0:
                        self.livingspace_with_space.append(\
                            current_room.room_name)
            con_people = new_session.query(PersonModel)
            people_list = con_people.all()
            for person in people_list:
                self.people.append({'person': person.name, 'types': \
                 person.position, 'accomodate': person.accomodate})
            self.rooms = self.offices + self.livingspace
            self.changes = False
            return "Successfully loaded."
        except OperationalError:
            return db + " does not exist."

    def save_state(self, db):
        """Writes changes to database"""
        if self.changes:
            self.changes = False
            engine = create_engine(\
            "sqlite:////Users/olivermunala/Desktop/Amity/amity/app/database/" \
            + db + ".db")
            session = sessionmaker(bind=engine)
            new_session = session()
            Base.metadata.create_all(engine)
            for person in self.new_persons:
                if person['position'] == "FELLOW":
                    new_fellow = Fellow(person['person'], person['position'],\
                    person['accomodate'])
                    new_fellow.add(person['person'])
                    new_fellow.add_person(person['person'], person['position'],\
                    person['accomodate'])
                else:
                    new_staff = Staff(person['person'], person['position'],\
                    person['accomodate'])
                    new_staff.add(person['person'])
                    new_staff.add_person(person['person'], person['position'],\
                    person['accomodate'])
            for room in self.new_rooms:
                if room['types'] == "office":
                    new_room = Office(room['room'], room['types'])
                    new_room.add()
                elif room['types'] == "livingspace":
                    new_room = LivingSpace(room['room'], room['types'])
                    new_room.add()
            for allocation in self.allocations:
                stmt = update(RoomModel).\
                where(RoomModel.room_name == allocation['room']).\
                values({'occuppants': RoomModel.occuppants + "," + \
                                       allocation['occupant'], \
                'space' : self.space[allocation['room']]})
                new_session.execute(stmt)
                new_session.commit()
            for real in self.reallocat:
                current_room = ""
                new_room = ""
                new_occupants_current = ""
                new_occupants_new = ""
                for roomy in self.rooms:
                    if roomy['room'] == real['current']:
                        new_occupants_current =\
                            roomy['occupants'].replace("," + real['person'], "")
                        current_room = roomy['room']
                        break
                for roomy in self.rooms:
                    if roomy['room'] == real['new']:
                        new_occupants_new = \
                            roomy['occupants'] + "," + real['person']
                        new_room = roomy['room']
                        break
                stmt = update(RoomModel).where(\
                    RoomModel.room_name==real['current'])\
                    .values({'occuppants': new_occupants_current,\
                             'space': self.space[current_room]})
                new_session.execute(stmt)
                new_session.commit()
                stmt = update(RoomModel).where(\
                    RoomModel.room_name==real['new'])\
                    .values({'occuppants': new_occupants_new,\
                             'space': self.space[new_room]})
                new_session.execute(stmt)
                new_session.commit()
                self.changes = False
            return "Successfully saved."
        else:
            return "No changes have been made for saving."

    def print_room(self, room):
        """Prints list of people in room"""
        found = False
        people_list = ""
        for rooms in self.offices:
            if rooms['room'] == room:
                people_list += (rooms['occupants'] + ", ")
                found = True
        for rooms in self.livingspace:
            if rooms['room'] == room:
                people_list += (rooms['occupants'] + ", ")
                found = True
        if not found:
            return "Room not found"
        else:
            return people_list
