"""
Usage:
  main.py create_room <room_name>...
  main.py add_person <fname> <lname> <type> [--wants_accommodation]
  main.py reallocate_person <fname> <lname> <new_room_name>
  main.py load_people
  main.py print_allocations [--o=filename]
  main.py print_unallocated [--o=filename]
  main.py print_room <room_name>
  main.py allocate_office <fname> <lname>
  main.py allocate_livingspace <fname> <lname>
  main.py save_state [--db=sqlite_database]
  main.py load_state <sqlite_database>
  main.py deallocate_person <fname> <lname> <room_type>
  main.py quit
  main.py reset
  main.py clear
  main.py ( -h | --help)
  main.py ( -i | --interactive)

Options:
  -h --help         Show this screen
  -i --interactive
"""

import sys
import cmd
import os
import time
from docopt import docopt, DocoptExit
from colorama import init
from pyfiglet import Figlet
from termcolor import colored

from app.classes.amity import Amity

init()
font = Figlet(font = 'starwars')
introd = font.renderText('Amity')
os.system('clear')
print(introd)


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

class AmityCli(cmd.Cmd):
    amity = Amity()
    amity.load_state("amity")
    prompt = 'Amity>> '
    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_name>..."""
        try:
            print(self.amity.create_room(arg['<room_name>']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <fname> <lname> <type> [--wants_accommodation=N]"""
        try:
            if arg['--wants_accommodation'] == "Y" or \
            arg['--wants_accommodation'] == "N" or \
            arg['--wants_accommodation'] == "" or \
            arg['--wants_accommodation'] == None:
                print(self.amity.add_person(arg['<fname>'], arg['<lname>'], \
                arg['<type>'].upper(), arg['--wants_accommodation']))
                print(self.amity.allocate_person_office(arg['<fname>'], \
                arg['<lname>']))
                if arg['<type>'].upper() == "FELLOW" and \
                arg['--wants_accommodation'] == "Y":
                    print(self.amity.allocate_person_livingspace(arg['<fname>'],\
                    arg['<lname>']))
            else:
                print("--wants_accommodation can only be Y or N")
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <fname> <lname> <new_room_name>"""
        try:
            print(self.amity.reallocate(arg['<fname>'], \
            arg['<lname>'], arg['<new_room_name>']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people"""
        print(self.amity.load())

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=allocations]"""
        try:
            if not arg['--o'] == None:
                if len(arg['--o'])>0:
                    print(self.amity.print_allocations(arg['--o']))
                else:
                    print("Add a file name when using --o.")
            else:
                print(self.amity.print_allocations(arg['--o']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""
        try:
            if not arg['--o'] == None:
                if len(arg['--o'])>0:
                    print(self.amity.print_unallocated(arg['--o']))
                else:
                    print("Add a file name when using --o.")
            else:
                print(self.amity.print_unallocated(arg['--o']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        try:
            print(self.amity.print_room(arg['<room_name>']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=amity]"""
        try:
            if not arg['--db'] == None:
                if len(arg['--db'])>0:
                    print(self.amity.save_state(arg['--db']))
                else:
                    print("Add a database name when using --db.")
            else:
                print(self.amity.save_state(arg['--db']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>"""
        try:
            print(self.amity.load_state(arg['<sqlite_database>']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_quit(self, arg):
        """Usage: quit"""
        if self.amity.changes:
            choice = input("Save changes? (Y/N): ").upper()
            if choice == "Y":
                self.amity.save_state("amity")
                print('Saved changes.')
                exit()
            elif choice == "N":
                print('System closed.')
                exit()
            else:
                print("Invalid choice. Enter Y for YES or N for NO.")
        else:
            print('System closed.')
            exit()

    @docopt_cmd
    def do_clear(self, arg):
        """Usage: clear"""
        os.system('clear')
        print(introd)
        prompt = 'Amity>> '

    @docopt_cmd
    def do_deallocate_person(self, arg):
        """Usage: deallocate_person <fname> <lname> <room_type>"""
        try:
            print(self.amity.deallocate_person(arg['<fname>'], arg['<lname>'], \
            arg['<room_type>'].lower()))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_allocate_office(self, arg):
        """Usage: allocate_office <fname> <lname>"""
        try:
            print(self.amity.allocate_person_office(\
                arg['<fname>'], arg['<lname>']))
        except ValueError:
            print("Load state first")

    @docopt_cmd
    def do_allocate_livingspace(self, arg):
        """Usage: allocate_livingspace <fname> <lname>"""
        try:
            print(self.amity.allocate_person_livingspace(\
                arg['<fname>'], arg['<lname>']))
        except ValueError:
            print("Load state first")

    @docopt_cmd
    def do_reset(self, arg):
        """Usage: reset"""
        os.system('clear')
        print("Resetting.")
        time.sleep(0.6)
        os.system('clear')
        print("Resetting..")
        time.sleep(0.6)
        os.system('clear')
        print("Resetting...")
        time.sleep(0.6)
        os.system('clear')
        self.amity.new_rooms = []
        self.amity.new_persons = []
        self.amity.offices = []
        self.amity.livingspace = []
        self.amity.rooms = []
        self.amity.people = []
        self.amity.allocations = []
        self.amity.allocated_office = []
        self.amity.allocated_living = []
        self.amity.offices_with_space = []
        self.amity.livingspace_with_space = []
        self.amity.space = {}
        self.amity.reallocation = []
        self.amity.reallocat = []
        self.amity.deallocated = []
        self.amity.changes = False
        self.amity.loaded = False
        print(introd)
        AmityCli().cmdloop()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    print(__doc__)
    try:
        AmityCli().cmdloop()
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt")
        exit()
