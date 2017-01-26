"""
Usage:
  main.py create_room <room_name>...
  main.py add_person <first_name> <last_name> <type> [--accommodate=N]
  main.py reallocate_person <first_name> <last_name> <new_room_name>
  main.py load_people
  main.py print_allocations [--o=file_name]
  main.py print_unallocated [--o=file_name]
  main.py print_room <room_name>
  main.py allocate_office <first_name> <last_name>
  main.py allocate_livingspace <first_name> <last_name>
  main.py save_state [--db=sqlite_database]
  main.py load_state <sqlite_database>
  main.py deallocate_person <first_name> <last_name> <room_type>
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
from termcolor import colored, cprint

from app.classes.amity import Amity

init()
font = Figlet(font = 'starwars')
title = font.renderText('Amity')
os.system('clear')
cprint(title)


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

            cprint('Invalid Command!', 'red')
            cprint(e, 'red')
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
        """
        Usage: create_room <room_name>...
        """
        try:
            cprint(self.amity.create_room(arg['<room_name>']), 'cyan')
        except ValueError:
            cprint("Invalid argument", 'red')

    @docopt_cmd
    def do_add_person(self, arg):
        """
        Usage: add_person <first_name> <last_name> <type> [--accommodate=N]
        """
        try:
            if arg['--accommodate'] == "Y" or \
            arg['--accommodate'] == "N" or \
            arg['--accommodate'] == "" or \
            arg['--accommodate'] == None:
                cprint(self.amity.add_person(arg['<first_name>'],\
                                            arg['<last_name>'],\
                                            arg['<type>'].upper(),\
                                            arg['--accommodate']), 'cyan')
                cprint(self.amity.allocate_person_office(arg['<first_name>'],\
                                                        arg['<last_name>']),
                       'cyan')
                if arg['<type>'].upper() == "FELLOW" \
                and arg['--accommodate'] == "Y":
                    cprint(self.amity.allocate_person_livingspace(\
                           arg['<first_name>'], arg['<last_name>']),
                           'cyan')
            else:
                cprint("--accommodate can only be Y or N", 'red')
        except ValueError:
            cprint("Invalid argument", 'red')

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """
        Usage: reallocate_person <first_name> <last_name> <new_room_name>
        """
        try:
            cprint(self.amity.reallocate(arg['<first_name>'],\
                                        arg['<last_name>'],\
                                        arg['<new_room_name>']),
                   'cyan')
        except ValueError:
            cprint("Invalid argument", 'red')

    @docopt_cmd
    def do_load_people(self, arg):
        """
        Usage: load_people
        """
        cprint(self.amity.load(), 'cyan')

    @docopt_cmd
    def do_print_allocations(self, arg):
        """
        Usage: print_allocations [--o=file_name]
        """
        try:
            if not arg['--o'] == None:
                if len(arg['--o']) > 0:
                    cprint(self.amity.print_allocations(arg['--o']), 'cyan')
                else:
                    cprint("Add a file name when using --o.", 'red')
            else:
                cprint(self.amity.print_allocations(arg['--o']), 'cyan')
        except ValueError:
            cprint("Invalid argument", 'red')

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """
        Usage: print_unallocated [--o=file_name]
        """
        try:
            if not arg['--o'] == None:
                if len(arg['--o']) > 0:
                    cprint(self.amity.print_unallocated(arg['--o']), 'cyan')
                else:
                    cprint("Add a file name when using --o.", 'red')
            else:
                cprint(self.amity.print_unallocated(arg['--o']), 'cyan')
        except ValueError:
            cprint("Invalid argument", 'red')

    @docopt_cmd
    def do_print_room(self, arg):
        """
        Usage: print_room <room_name>
        """
        try:
            cprint(self.amity.print_room(arg['<room_name>']), 'cyan')
        except ValueError:
            cprint("Invalid argument", 'red')

    @docopt_cmd
    def do_save_state(self, arg):
        """
        Usage: save_state [--db=amity]
        """
        try:
            if not arg['--db'] == None:
                if len(arg['--db']) > 0:
                    cprint(self.amity.save_state(arg['--db']), 'cyan')
                else:
                    cprint("Add a database name when using --db.", 'red')
            else:
                cprint(self.amity.save_state(arg['--db']), 'cyan')
        except ValueError:
            cprint("Invalid argument", 'red')

    @docopt_cmd
    def do_load_state(self, arg):
        """
        Usage: load_state <sqlite_database>
        """
        try:
            cprint(self.amity.load_state(arg['<sqlite_database>']), 'cyan')
        except ValueError:
            cprint("Invalid argument", 'red')

    @docopt_cmd
    def do_quit(self, arg):
        """
        Usage: quit
        """
        if self.amity.changes:
            choice = input("Save changes? (Y/N): ").upper()
            if choice == "Y":
                self.amity.save_state("amity")
                cprint('Saved changes.', 'cyan')
                exit()
            elif choice == "N":
                cprint('System closed.', 'green')
                exit()
            else:
                cprint("Invalid choice. Enter Y for YES or N for NO.", 'red')
        else:
            cprint('System closed.', 'green')
            exit()

    @docopt_cmd
    def do_clear(self, arg):
        """
        Usage: clear
        """
        os.system('clear')
        cprint(title, 'green')
        prompt = 'Amity>> '

    @docopt_cmd
    def do_deallocate_person(self, arg):
        """
        Usage: deallocate_person <first_name> <last_name> <room_type>
        """
        try:
            cprint(self.amity.deallocate_person(arg['<first_name>'],\
                                               arg['<last_name>'],\
                                               arg['<room_type>'].lower()),
                   'cyan')
        except ValueError:
            cprint("Invalid argument", 'red')

    @docopt_cmd
    def do_allocate_office(self, arg):
        """
        Usage: allocate_office <first_name> <last_name>
        """
        try:
            cprint(self.amity.allocate_person_office(arg['<first_name>'],\
                                                    arg['<last_name>']),
                   'cyan')
        except ValueError:
            cprint("Load state first", 'Yyellow')

    @docopt_cmd
    def do_allocate_livingspace(self, arg):
        """
        Usage: allocate_livingspace <first_name> <last_name>
        """
        try:
            cprint(self.amity.allocate_person_livingspace(arg['<first_name>'],\
                                                         arg['<last_name>']),
                   'cyan')
        except ValueError:
            cprint("Load state first", 'yellow')

    @docopt_cmd
    def do_reset(self, arg):
        """
        Usage: reset
        """
        os.system('clear')
        cprint("Resetting.", 'cyan')
        time.sleep(0.6)
        os.system('clear')
        cprint("Resetting..", 'yellow')
        time.sleep(0.6)
        os.system('clear')
        cprint("Resetting...", 'green')
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
        self.amity.reallocated_people = []
        self.amity.deallocated_people = []
        self.amity.changes = False
        self.amity.loaded = False
        cprint(title)
        AmityCli().cmdloop()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    cprint(__doc__)
    try:
        AmityCli().cmdloop()
    except KeyboardInterrupt:
        cprint("\nKeyboard Interrupt", 'red')
        exit()
