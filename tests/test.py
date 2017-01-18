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

class Tester(TestCase):
    """Holds all tests"""
    def test_main_function_type(self):
        """Tests for object type"""
        am = Amity()
        self.assertTrue(isinstance(am, Amity))

    def test_add_person(self):
        """Tests for add_person function"""
        am = Amity()
        self.assertEqual(am.add_person("Ngoitsi_Oliver", "FELLOW", "N"), \
                         "Successfully added Ngoitsi Oliver")

    def test_add_room(self):
        """Tests for add_room function"""
        with patch('builtins.input', return_value='office'):
            am = Amity()
            self.assertEqual(am.create_room(["Roundtable"]), \
                            "\nSuccessfully added Roundtable")

    def test_add_room_exists(self):
        """Tests for add_room function"""
        with patch('builtins.input', return_value='office'):
            am = Amity()
            am.load_state("amity")
            self.assertEqual(am.create_room(["Valhalla"]), \
                            "Valhalla already exists")

    def test_add_room_wrong_type(self):
        """Tests for add_room function"""
        with patch('builtins.input', return_value='off'):
            am = Amity()
            self.assertEqual(am.create_room(["Roundtable"]), \
                            "\nRoundtable can only be office or livingspace")

    def test_reallocation(self):
        """Tests for reallocate function"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.reallocate("Olivers_Munala", "Valhalla"), \
                         "Olivers Munala has been reallocated to Valhalla")

    def test_load(self):
        """Tests for load function"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.load(), "Successfully loaded.")

    def test_print_allocations(self):
        """Tests for print_allocations function"""
        am = Amity()
        self.assertIn("", am.print_allocations("o"))

    def test_print_unallocationed(self):
        """Tests for print_unallocated function"""
        am = Amity()
        self.assertIn(r" ", am.print_unallocated("o"))

    def test_print_room(self):
        """Tests for print_room function"""
        am = Amity()
        self.assertIn(r" ", am.print_room("Valhalla"))

    def test_load_state(self):
        """Tests for load_state function"""
        am = Amity()
        self.assertEqual(am.load_state("amity"), "Successfully loaded.")

    def test_save_state(self):
        """Tests for save_state function"""
        am = Amity()
        self.assertEqual(am.save_state("amity"), \
        "No changes have been made for saving.")

    def test_inheritance_office(self):
        """Tests for inheritance"""
        room = Office("Valhalla", "Office")
        self.assertTrue(isinstance(room, Room))

    def test_inheritance_livingspace(self):
        """Tests for inheritance"""
        room = Office("Home", "livingspace")
        self.assertTrue(isinstance(room, Room))

    def test_inheritance_fellow(self):
        """Tests for inheritance"""
        person = Fellow("Oliver_Munala", "FELLOW", "N")
        self.assertTrue(isinstance(person, Person))

    def test_inheritance_staff(self):
        """Tests for inheritance"""
        person = Staff("Oliver_Munala", "STAFF", "N")
        self.assertTrue(isinstance(person, Person))

    def test_exists_person(self):
        """Tests for existence of person"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.add_person("Olivers_Munala", "FELLOW", "N"), \
        "Person already exists")

    def test_input_person(self):
        """Tests for valid input"""
        am = Amity()
        self.assertEqual(am.add_person("Munlaz_Verulo", "st", "N"), \
        "Wrong input. Can only be FELLOW or STAFF")

    def test_room_not_found(self):
        """Tests for existing room"""
        am = Amity()
        self.assertEqual(am.print_room("fefe"), "Room not found")

    def test_room_exists(self):
        """Tests for existing room"""
        am = Amity()
        self.assertEqual(am.create_room(["Valhalla"]), "Valhalla already exists")
