"""Test class module"""
from unittest import TestCase
from unittest.mock import patch

from app.classes.person import Person
from app.classes.amity import Amity
from app.classes.room import Room
from app.classes.fellow import Fellow
from app.classes.staff import Staff
from app.classes.office import Office
from app.classes.livingspace import LivingSpace
from app.models.models import *

class TestAddingPerson(TestCase):
    """Holds all tests for adding person"""
    def setUp(self):
        self.amity = Amity()

    def test_successfully_adding_person(self):
        """Tests for adding person successfully"""
        self.amity.load_state("amity")
        self.assertIn("Successfully added NGOITSI OLIVER",\
        self.amity.add_person("Ngoitsi", "Oliver", "FELLOW", "N"))

    def test_adding_person_who_exists_in_amity(self):
        """Tests for adding person who has already been added"""
        with patch('builtins.input', return_value='N'):
            self.amity.load_state("amity")
            self.assertEqual(self.amity.add_person(\
            "TANA", "LOPEZ", "FELLOW", "N"),\
            "Operation cancelled.")

    def test_adding_person_who_exists_in_amity(self):
        """Tests for adding person who has already been added"""
        with patch('builtins.input', return_value='Y'):
            self.amity.load_state("amity")
            self.assertIn("Successfully added TANA LOPEZ",\
            self.amity.add_person("TANA", "LOPEZ", "FELLOW", "N"))

    def test_adding_person_with_invalid_position(self):
        """Tests adding person who's position is not staff or fellow"""
        self.amity.load_state("amity")
        self.assertEqual(self.amity.add_person("Munlaz", "Verulo", "st", "N"),\
                         "Wrong input. Can only be FELLOW or STAFF")


class TestAddingRoom(TestCase):
    """Holds all tests for adding rooms"""
    def setUp(self):
        self.amity = Amity()

    def test_successfully_adding_room(self):
        """Tests for adding room successfully"""
        with patch('builtins.input', return_value='office'):
            self.assertEqual(self.amity.create_room(["Roundtable"]),\
                             "\nSuccessfully added Roundtable")

    def test_adding_room_that_exists_in_amity(self):
        """Tests for adding room that already exists"""
        with patch('builtins.input', return_value='office'):
            self.amity.load_state("amity")
            self.assertEqual(self.amity.create_room(["Valhalla"]),\
                             "Valhalla already exists")

    def test_adding_room_with_wrong_room_type(self):
        """Tests for adding room with wrong room type"""
        with patch('builtins.input', return_value='off'):
            self.assertEqual(self.amity.create_room(["Roundtable"]),\
                             "\nRoundtable can only be office or livingspace")

class TestAllocatingRoom(TestCase):
    """Holds all tests for allocating rooms"""
    def setUp(self):
        self.amity = Amity()

    def test_allocating_office_successfully(self):
        """Tests for allocating an office successfully"""
        self.amity.load_state("amity")
        self.assertIn("Successfully allocated KEVIN MUNALA",\
                      self.amity.allocate_person_office("KM16"))

    def test_allocating_office_to_already_allocated_person(self):
        """
        Tests for allocating an office to a person who has an office already
        """
        self.amity.load_state("amity")
        self.assertEqual(self.amity.allocate_person_office("TL6"),\
                         "TANA LOPEZ has already been allocated an office.")

    def test_allocating_office_to_person_who_does_not_exist(self):
        """Tests for allocatin an office to person who does not exist"""
        self.amity.load_state("amity")
        self.assertEqual(self.amity.allocate_person_office("TD6"),\
                         "Person does not exist. Cannot allocate office.")

    def test_allocatiing_livingspace_successfully(self):
        """Tests for allocating a livingspace successfully"""
        self.amity.load_state("amity")
        self.assertIn("Successfully allocated Oliver Munala",\
                      self.amity.allocate_person_livingspace("OM14"))

    def test_allocating_livingspace_to_already_allocated_person(self):
        """
        Tests for allocating a livingspace to person who has an office already
        """
        self.amity.load_state("amity")
        self.assertEqual(self.amity.allocate_person_livingspace("MY22"),\
                         "me yous has already been allocated a living space.")

    def test_allocating_livingspace_to_person_who_does_not_exist(self):
        """Tests for allocatin a livingspace to person who does not exist"""
        self.amity.load_state("amity")
        self.assertEqual(self.amity.allocate_person_livingspace("TD6"),\
                         "Person does not exist. Cannot allocate living space.")

    def test_allocating_livingspace_to_staff(self):
        """Tests for allocatin a livingspace to staff member"""
        self.amity.load_state("amity")
        self.assertEqual(self.amity.allocate_person_livingspace("GG23"),\
                         "Living spaces are for fellows only")

class TestReallocatingRoom(TestCase):
    """Holds all tests for reallocating rooms"""
    def setUp(self):
        self.amity = Amity()

    def test_reallocating_person_successfully(self):
        """Tests for reallocating person successfully"""
        self.amity.load_state("amity")
        self.assertEqual(self.amity.reallocate("TL6", "Occulus"),\
                         "TANA LOPEZ has been reallocated to Occulus")

    def test_reallocating_person_to_full_room(self):
        """Tests for reallocating person to a room with no space"""
        self.amity.load_state("amity")
        self.assertEqual(self.amity.reallocate("TL6", "Valhalla"),\
                         "Valhalla is full.")

    def test_reallocating_person_to_missing_room(self):
        """Tests for reallocating person to a room that does not exist"""
        self.amity.load_state("amity")
        self.assertEqual(self.amity.reallocate("TL6", "hsssog"),\
                         "hsssog does not exist.")

    def test_reallocating_person_who_does_not_exist(self):
        """Tests for reallocating person who does not exist"""
        self.amity.load_state("amity")
        self.assertEqual(self.amity.reallocate("TD6", "Valhalla"),\
                         "Person does not exist")

    def test_already_allocated_person_to_current_room(self):
        """Tests for reallocating person to his/her current room"""
        self.amity.load_state("amity")
        self.assertEqual(self.amity.reallocate("OM15",\
                                               "Hogwarts"),\
                         "Olivers Munala has already" + \
                         " been allocated to Hogwarts")

class TestLoadingPeople(TestCase):
    """Holds all tests for loading people"""
    def setUp(self):
        self.amity = Amity()

    def test_load_successful(self):
        """Tests for loading people successfully"""
        self.amity.load_state("amity")
        self.assertEqual(self.amity.load_people(), "Successfully loaded.")

class TestPrintingAllocations(TestCase):
    """Holds all tests for printing room allocations"""
    def setUp(self):
        self.amity = Amity()

    def test_print_allocations_successfully(self):
        """Tests for prining allocations successfully"""
        self.amity.load_state("amity")
        self.assertIn("Valhalla", self.amity.print_allocations("o"))

class TestPrintingUnallocatedPeople(TestCase):
    """Holds all tests for printing unallocated people"""
    def setUp(self):
        self.amity = Amity()

    def test_print_unallocated_people_successfully(self):
        """Tests for printing unallocated people successfully"""
        self.amity.load_state("amity")
        self.assertIn("Unallocated", self.amity.print_unallocated("o"))

class TestPrintingRoomOccupants(TestCase):
    """Holds all tests for printing room occupants"""
    def setUp(self):
        self.amity = Amity()

    def test_printing_room_successfully(self):
        """Tests for printing room successfully"""
        self.amity.load_state("amity")
        self.assertIn("Valhalla", self.amity.print_room("Valhalla"))

    def test_printing_missing_room(self):
        """Tests for printing room that does not exist"""
        self.assertEqual(self.amity.print_room("fefe"), "Room not found")

class TestLoadingState(TestCase):
    """Holds all tests for loading state"""
    def setUp(self):
        self.amity = Amity()

    def test_loading_state_successfully(self):
        """Tests for loading state successfully"""
        self.assertEqual(self.amity.load_state("amity"), "Successfully loaded.")

    def test_loading_state_with_missing_database(self):
        """Tests for loading state with a database that does not exist"""
        self.assertEqual(self.amity.load_state("abcd"), "abcd does not exist.")

class TestSavingState(TestCase):
    """Holds all tests for saving state"""
    def setUp(self):
        self.amity = Amity()

    def test_saving_state_without_changes(self):
        """Tests for saving state function without changes"""
        self.assertEqual(self.amity.changes, False)

    def test_saving_state_successfully(self):
        """Tests for saving state function without changes"""
        self.amity.load_state("amity")
        self.amity.add_person("Oliver", "Munlaz", "FELLOW", "N")
        self.assertEqual(self.amity.changes, True)
