"""Test class module"""
from unittest import TestCase
import mock

from main import MainFunctions
from classes.person import *
from classes.staff import *
from classes.fellow import *
from classes.room import *
from classes.livingspace import *
from classes.office import *

class Tester(TestCase):
    """Holds all tests"""
    def test_main_function_type(self):
        """Tests for object type"""
        am = MainFunctions()
        self.assertTrue(isinstance(am, MainFunctions))

    def test_add_person(self):
        """Tests for add_person function"""
        am = MainFunctions()
        self.assertEqual(am.add_person("Ngoitsi", "FELLOW", "N"), \
                         "Successfully added Ngoitsi")

    def test_add_room(self):
        """Tests for add_room function"""
        am = MainFunctions()
        with mock.patch('builtins.input', return_value='office'):
            self.assertEqual(am.create_room(["Hogwarts"]), \
                             "Successfully added Hogwarts")

    def test_reallocation(self):
        """Tests for reallocate function"""
        am = MainFunctions()
        self.assertEqual(am.reallocate("Kevin"), \
                         "Person does not exist")

    def test_load(self):
        """Tests for load function"""
        am = MainFunctions()
        self.assertEqual(am.load(), "Successfully loaded.")

    def test_print_allocations(self):
        """Tests for print_allocations function"""
        am = MainFunctions()
        self.assertIn("", am.print_allocations("o"))

    def test_print_unallocationed(self):
        """Tests for print_unallocated function"""
        am = MainFunctions()
        self.assertIn(r" ", am.print_unallocated("o"))

    def test_print_room(self):
        """Tests for print_room function"""
        am = MainFunctions()
        self.assertIn(r" ", am.print_room("Valhalla"))

    def test_load_state(self):
        """Tests for load_state function"""
        am = MainFunctions()
        self.assertEqual(am.load_state(), "Successfully loaded.")

    def test_save_state(self):
        """Tests for save_state function"""
        am = MainFunctions()
        self.assertEqual(am.save_state(), "Successfully saved.")

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
        person = Fellow("Oliver", "FELLOW", "N")
        self.assertTrue(isinstance(person, Person))

    def test_inheritance_staff(self):
        """Tests for inheritance"""
        person = Staff("Oliver", "STAFF", "N")
        self.assertTrue(isinstance(person, Person))

    def test_inheritance_person(self):
        """Tests for inheritance"""
        person = Person("Oliver", "STAFF", "N")
        self.assertTrue(isinstance(person, Amity))

    def test_exists_person(self):
        """Tests for inheritance"""
        am = MainFunctions()
        self.assertEqual(am.add_person("Oliver", "st", "N"), "Person already exists")

    def test_input_person(self):
        """Tests for inheritance"""
        am = MainFunctions()
        self.assertEqual(am.add_person("Munlaz", "st", "N"), "Wrong input. Can only be FELLOW or STAFF")

    def test_room_not_found(self):
        """Tests for inheritance"""
        am = MainFunctions()
        self.assertEqual(am.print_room("fefe"), "Room not found")

    def test_room_exists(self):
        """Tests for inheritance"""
        am = MainFunctions()
        self.assertEqual(am.create_room(["Valhalla"]), "Valhalla already exists")