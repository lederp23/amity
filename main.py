"""Main class module"""
from random import randint
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, update

from classes.fellow import *
from classes.livingspace import *
from classes.office import *
from classes.person import *
from classes.room import *
from classes.staff import *
from models.models import *

class MainFunctions:
    """Contains main functions"""
    details = []
    new_rooms = []
    new_persons = []
    offices = []
    livingspace = []
    people = []
    allocations = []
    allocated_office = []
    allocated_living = []
    offices_with_space = []
    livingspace_with_space = []
    space = {}

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
                    msg = "Successfully added " + room[count]
                else:
                    msg = "Room can only be office or livingspace"
        return msg

    def add_person(self, name, pos, accomodation):
        """Adds person"""
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
                return "Successfully added " + name
            else:
                return "Wrong input. Can only be FELLOW or STAFF"

    def reallocate(self, person):
        """Reassigns a person to a different room"""
        pos = ""
        accomodate = "N"
        found = False
        for persons in self.people:
            if persons['person'] == person:
                pos = persons['types']
                accomodate = persons['accomodate']
                found = True
        if found:
            for space in self.livingspace:
                for occ in space['occupants']:
                    if person in occ:
                        try:
                            occ.remove(person)
                            space['space'] += 1
                        except ValueError:
                            pass
            for off in self.offices:
                for occ in off['occupants']:
                    if person in occ:
                        try:
                            occ.remove(person)
                            space['space'] += 1
                        except ValueError:
                            pass
            for alloc in self.allocations:
                if alloc['occupant'] == person:
                    try:
                        self.allocations.remove(alloc)
                    except ValueError:
                        pass
                    return self.allocate_person(person, pos, accomodate)
        else:
            return "Person does not exist"

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

        if option == "o":
            files = open("allocations.txt", "w")
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
        if option == "o":
            files = open("unallocated.txt", "w")
            files.write(unallocated)
            files.close()
        if unallocated == "":
            return "No one is missing a room"
        else:
            return unallocated

    def load(self):
        """Loads people from txt file"""
        accomodate = ""
        individual = []
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
            print(self.allocate_person(name, types, accomodate))
        return "Successfully loaded."

    def allocate_person(self, name, types, accomodate):
        """Allocates room"""
        exists = False
        accom = ""
        for person in self.people:
            if name == person['person']:
                types = person['types']
                accom = person['accomodate']
                exists = True
        if exists:
            if not name in self.allocated_office:
                room_number = randint(0, (len(self.offices)-1))
                current_room = self.offices[room_number]
                if len(self.offices_with_space) < 1:
                        print("There is no office with space")
                else:
                    if self.space[current_room['room']] > 0:
                        new_occupants = current_room['occupants'] + name
                        current_room['occupants'] = new_occupants
                        self.space[current_room['room']] -= 1
                        self.offices[room_number] = current_room
                        self.allocations.append({'room':\
                        current_room['room'], 'occupant': name})
                        self.allocated_office.append(name)
                        return "Successfully allocated " + name
                    else:
                        try:
                            self.offices_with_space.remove(\
                                current_room['room'])
                            self.allocate_person(name, types, accomodate)
                        except ValueError:
                            pass
            if types == "FELLOW" and types == "FELLOW":
                if not name in self.allocated_living:
                    if len(self.livingspace) < 1:
                        return "There is no livingspace with space"
                    else:
                        if accomodate == "Y" and accom == "Y":
                            if current_room['space'] > 0:
                                room_number = randint(\
                                    0, (len(self.livingspace)- 1))
                                current_room = self.livingspace[room_number]
                                new_occupants = current_room['occupants'] +\
                                                name
                                current_room['occupants'] = new_occupants
                                current_room['space'] -= 1
                                self.offices[room_number] = current_room
                                self.allocations.append(\
                                    {'room': current_room['room'],\
                                     'occupant': name})
                                return name + " has been allocated to " +\
                                      current_room['room']
                                self.allocated_living.append(name)
                            else:
                                try:
                                    self.livingspace_with_space.remove(\
                                        current_room['room'])
                                except ValueError:
                                    pass
                                self.allocate_person(name, types,\
                                                     accomodate)
                        else:
                            return "Inconsistency between data provided \
                            and database."
                else:
                    return name + " has already been allocated"
        else:
            self.add_person(name, types, accomodate)
            self.allocate_person(name, types, accomodate)

    def load_state(self):
        """Loads data from database"""
        engine = create_engine("sqlite:///D:/code/amity/database/amity.db")
        session = sessionmaker(bind=engine)
        new_session = session()
        con_room = new_session.query(RoomModel)
        room_list = con_room.all()
        for current_room in room_list:
            self.space.update({current_room.room_name: current_room.space})
            if len(current_room.occuppants)> 1:
                for occ in current_room.occuppants.split(","):
                    self.allocations.append({'room': current_room.room_name, \
                                         'occupant': occ\
                                             })
            if current_room.roomType == 'office':
                self.offices.append({'room': current_room.room_name,\
                'types': current_room.roomType, 'max': \
                current_room.maximum_capacity, 'space': \
                int(current_room.space), 'occupants': \
                current_room.occuppants})
                allocatedd = current_room.occuppants.split(",")
                self.allocated_office += allocatedd
                if current_room.space > 0:
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
        return "Successfully loaded."

    def save_state(self):
        """Writes changes to database"""
        engine = create_engine("sqlite:///D:/code/amity/database/amity.db")
        session = sessionmaker(bind=engine)
        new_session = session()
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
            else:
                print("Can only be office or livingspace")
        new_alloc = ""
        for allocation in self.allocations:
            new_alloc += ("," + allocation['occupant'])
            stmt = update(RoomModel).\
            where(RoomModel.room_name == allocation['room']).\
            values({'occuppants' : new_alloc[1:], \
            'space' : self.space[allocation['room']]})
            new_session.execute(stmt)
            new_session.commit()
        return "Successfully saved."

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


x = MainFunctions()
x.load_state()
print(x.load())
x.save_state()