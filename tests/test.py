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
        """Tests for add_person success"""
        am = Amity()
        self.assertEqual(am.add_person("Ngoitsi_Oliver", "FELLOW", "N"), \
                         "Successfully added Ngoitsi Oliver")

    def test_add_person_names(self):
        """Tests for add_person with one name"""
        am = Amity()
        self.assertEqual(am.add_person("Ngoitsi", "FELLOW", "N"), \
                         "Both first name and last name are required")

    def test_add_room(self):
        """Tests for add_room success"""
        with patch('builtins.input', return_value='office'):
            am = Amity()
            self.assertEqual(am.create_room(["Roundtable"]), \
                            "\nSuccessfully added Roundtable")

    def test_add_room_exists(self):
        """Tests for add_room if room exists"""
        with patch('builtins.input', return_value='office'):
            am = Amity()
            am.load_state("amity")
            self.assertEqual(am.create_room(["Valhalla"]), \
                            "Valhalla already exists")

    def test_add_room_wrong_type(self):
        """Tests for add_room wrong type"""
        with patch('builtins.input', return_value='off'):
            am = Amity()
            self.assertEqual(am.create_room(["Roundtable"]), \
                            "\nRoundtable can only be office or livingspace")

    def test_allocation_office(self):
        """Tests for allocate office, person already allocated"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.allocate_person_office("TANA LOPEZ"), \
                         "TANA LOPEZ has already been allocated an office.")

    def test_allocation_office_success(self):
        """Tests for allocate success"""
        am = Amity()
        am.load_state("amity")
        self.assertIn("Successfully allocated KEVIN MUNALA", \
                      am.allocate_person_office("KEVIN MUNALA"))

    def test_allocation_office_person_not_found(self):
        """Tests for allocate office, person not found"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.allocate_person_office("TANA aLOPEZ"), \
                         "Person does not exist")

    def test_allocation_office_success(self):
        """Tests for allocate success"""
        am = Amity()
        am.load_state("amity")
        self.assertIn("Successfully allocated Oliver Munala", \
                      am.allocate_person_office("Oliver Munala"))

    def test_allocation_livingspace(self):
        """Tests for allocate livingspace, person already allocated"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.allocate_person_livingspace("OLUWAFEMI SULE"), \
                 "OLUWAFEMI SULE has already been allocated a living space.")

    def test_allocation_livingspace_person_not_found(self):
        """Tests for allocate office, person not found"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.allocate_person_office("TANA aLOPEZ"), \
                         "Person does not exist")


    def test_allocation_livingspace_success(self):
        """Tests for allocate livingspace success"""
        am = Amity()
        am.load_state("amity")
        self.assertIn("Successfully allocated Oliver Munala", \
                      am.allocate_person_livingspace("Oliver Munala"))


    def test_reallocation(self):
        """Tests for reallocate success"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.reallocate("TANA_LOPEZ", "Occulus"), \
                         "TANA LOPEZ has been reallocated to Occulus")

    def test_reallocation_full(self):
        """Tests for reallocate, room full"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.reallocate("TANA_LOPEZ", "Valhalla"), \
                         "Valhalla is full.")

    def test_reallocation_exists(self):
        """Tests for reallocate, person does not exist"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.reallocate("TANA_LOPEddZ", "Valhalla"), \
                         "Person does not exist")

    def test_already_allocated(self):
        """Tests for reallocate, already allocated to room"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.reallocate("Olivers_Munala", "Hogwarts"), \
                         "Olivers Munala has already been allocated to Hogwarts")

    def test_load(self):
        """Tests for load success"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.load(), "Successfully loaded.")

    def test_print_allocations(self):
        """Tests for print_allocations success"""
        am = Amity()
        self.assertIn("", am.print_allocations("o"))

    def test_print_unallocationed(self):
        """Tests for print_unallocated success"""
        am = Amity()
        self.assertIn(r" ", am.print_unallocated("o"))

    def test_print_room(self):
        """Tests for print_room success"""
        am = Amity()
        self.assertIn(r" ", am.print_room("Valhalla"))

    def test_load_state(self):
        """Tests for load_state success"""
        am = Amity()
        self.assertEqual(am.load_state("amity"), "Successfully loaded.")

    def test_load_state_wrong_db(self):
        """Tests for load_state, wrong database"""
        am = Amity()
        self.assertEqual(am.load_state("aaaa"), "aaaa does not exist.")

    def test_save_state(self):
        """Tests for save_state function without changes"""
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

    def test_remove_person(self):
        """Test for removing person success"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.remove_person("KEVIN_MUNALA"), \
        "Successfully removed KEVIN MUNALA")

    def test_remove_person_not_found(self):
        """Test for removing person who does not exist"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.remove_person("defefee_feeffe"), \
        "defefee feeffe does not exist")

    def test_remove_person_one_name(self):
        """Test for remove person using one name"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.remove_person("Kevin"), \
        "Wrong name format")

    def test_remove_room(self):
        """Test for removing room"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.remove_room("PHP"), "Successfully removed PHP")

    def test_remove_room_not_found(self):
        """Test for removing room that does not exist"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.remove_room("aaa"), "aaa does not exist")

    def test_rename_room(self):
        """Test for renaming room"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.rename_room("PHP", "Python"), \
        "Successfully renamed")

    def test_rename_room_not_found(self):
        """Test for renaming room that does not exist"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.rename_room("js", "Python"), \
        "js does not exist")

    def test_rename_person(self):
        """Test for renaming person"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.rename_person("Olivers_Munala", "Oliverd_Munala"), \
        "Successfully renamed")

    def test_rename_person_not_found(self):
        """Test for renaming person that does not exist"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.rename_person("js_js", "Oliver_Munalas"), \
        "js js does not exist")

    def test_rename_person_wrong_format(self):
        """Test for renaming person with wrong name format"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.rename_person("Oliver", "Oliver_Munalas"), \
        "Wrong name format")
        self.assertEqual(am.rename_person("Olivers_Munala", "Oliver"), \
        "Wrong name format")
        self.assertEqual(am.rename_person("Munala", "Oliver"), \
        "Wrong name format")

    def test_rename_person_name_used(self):
        """Test for renaming person with name that exists"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.rename_person("Olivers_Munala", "TANA_LOPEZ"), \
        "Name already in use")

    def test_empty_room(self):
        """Test for emptying a room"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.empty_room("Valhalla"), "PHP is now empty")

    def test_empty_room(self):
        """Test for emptying a room which is empty"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.empty_room("PHP"), "PHP is already empty")

    def test_empty_room_not_found(self):
        """Test for emptying room that does not exist"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.empty_room("aaa"), "aaa does not exist")

    def test_deallocate_person(self):
        """Test for removing person from rooms"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.deallocate_person("Olivers_Munala", "office"), \
        "Successfully deallocated Olivers Munala")

    def test_deallocate_person_not_found(self):
        """Test for removing person from rooms"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.deallocate_person("Olivers_Munalas", "office"), \
        "Olivers Munalas does not exist")

    def test_deallocate_person_wrong_name_format(self):
        """Test for removing person from rooms with wrong name format"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.deallocate_person("Olivers", "office"), \
        "Wrong name format")

    def test_deallocate_person_wrong_type(self):
        """Test for removing person from rooms with wrong room type"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.deallocate_person("Olivers_Munala", "off"), \
        "Wrong room type")

    def test_deallocate_person_not_allocated(self):
        """Test for removing person who's not allocated"""
        am = Amity()
        am.load_state("amity")
        self.assertEqual(am.deallocate_person("KEVIN_MUNALA", "office"), \
        "KEVIN MUNALA has not been allocated")
